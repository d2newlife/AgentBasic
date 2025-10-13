import json
import ast
from typing import List, Dict, Any

def parse_json_response(log_string: str) -> List[Dict[str, Any]]:
    """
    Parses a string containing multiple dictionary-like objects where the 'output'
    field is itself a JSON string that needs to be nested.

    Args:
        log_string: A string where each line contains a dictionary string.
                    Example: "{'query': '...', 'output': '{\"topic\": \"...\"}'}"

    Returns:
        A list of dictionaries, where each entry combines the 'query' and the
        parsed content of the 'output' field.
    """
    
    # 1. Split the entire input string into individual lines/entries
    entries = log_string.strip().split('\n')
    
    parsed_results = []
    
    # 2. Process each entry
    for entry_string in entries:
        if not entry_string.strip():
            continue  # Skip empty lines
            
        try:
            # 3. Use ast.literal_eval to safely convert the outer Python dictionary
            #    string (which uses single quotes) into a Python dictionary object.
            #    This is much safer than using eval().
            outer_dict = ast.literal_eval(entry_string.strip())
            
            # Extract the necessary fields
            query = outer_dict.get('query')
            output_json_string = outer_dict.get('output')
            
            if not query or not output_json_string:
                print(f"Warning: Skipping entry due to missing 'query' or 'output': {entry_string[:50]}...")
                continue
                
            # 4. Use json.loads to parse the internal JSON string from the 'output' field.
            inner_data = json.loads(output_json_string)
            
            # 5. Combine the data: add the original query to the final result dictionary
            final_result = {
                'query': query,
                **inner_data # Merges all key-value pairs from the inner_data (topic, summary, etc.)
            }
            
            parsed_results.append(final_result)
            
        except (SyntaxError, ValueError, json.JSONDecodeError) as e:
            # Handle potential errors during parsing
            print(f"Error parsing entry: {entry_string[:50]}... Error: {e}")
            
    return parsed_results

# --- Example Usage ---

log_data = """
{'query': 'tell me about turtles', 'output': '{"topic": "Turtles", "summary": "Turtles are reptiles of the order Testudines, distinguished by a protective shell. They inhabit diverse environments globally and comprise over 300 species, including sea turtles, snapping turtles, and tortoises. Known for their longevity, turtles are ectothermic and have varied diets. They are ecologically significant, contributing to seed dispersal and nutrient cycling.", "sources": ["General knowledge"], "tools_used": ["save_text_to_file"]}\\n'}
{'query': 'tell me about sharks', 'output': '{"topic": "Sharks", "summary": "Sharks are a group of elasmobranch fish characterized by a cartilaginous skeleton, five to seven gill slits on the sides of the head, and pectoral fins that are not fused to the head. Modern sharks are classified within the clade Selachimorpha and are sister group to the batoids.", "sources": [], "tools_used": ["save_text_to_file"]}\\n'}
{'query': 'explain photosynthesis', 'output': '{"topic": "Photosynthesis", "summary": "Photosynthesis is the process used by plants, algae, and certain bacteria to convert light energy, usually from the Sun, into chemical energy that can be later released to fuel the organism\\'s activities. This energy is stored in carbohydrate molecules, such as sugars, which are synthesized from carbon dioxide and water.", "sources": ["General knowledge"], "tools_used": ["analyze_image"]}\\n'}
"""

parsed_output = parse_log_data(log_data)

# Print the structured, combined output
print("\n--- Parsed and Combined Output ---")
for item in parsed_output:
    print(f"Query: {item['query']}")
    print(f"Topic: {item['topic']}")
    print(f"Summary Start: {item['summary'][:50]}...")
    print(f"Sources: {item['sources']}")
    print("-" * 20)

# Optional: Print the full list for inspection
# import pprint
# print("\nFull List:")
# pprint.pprint(parsed_output)

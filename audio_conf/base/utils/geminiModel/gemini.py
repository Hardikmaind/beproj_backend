# import google.generativeai as genai
# import re

# # Set your Gemini API key here
# YOUR_API_KEY = "AIzaSyDKIARUcsy7sU9o5gkmFgg50YX-nY21Thg"

# # Configure the Gemini API with your API key
# genai.configure(api_key=YOUR_API_KEY)

# def rate_answer(question, user_answer, output_file):
#     # Initialize the Gemini model
#     model = genai.GenerativeModel('gemini-pro')

#     # Generate a prompt by combining the question and user's answer
#     prompt = f"Question: {question}\nAnswer: {user_answer}\n Rate the correctness of the answer out of 10."

#     # Generate content using the prompt
#     response = model.generate_content(prompt)

#     # Extract the rating from the response
#     rating = extract_rating(response.text)

#     # Write the rating to the output file if rating is 7 or greater
#     if rating is not None and rating >= 7:
#         try:
#             with open(output_file, 'w') as f:
#                 f.write(f"Rating: {rating}/10\n")
#         except OSError as e:
#             print(f"Error writing to file: {e}")
#     else:
#         # Write the Gemini model's response to the output file along with the rating if it's less than 7
#         try:
#             with open(output_file, 'w') as f:
                
#                 f.write("Suggestion:\n")
#                 f.write(response.text)
#         except OSError as e:
#             print(f"Error writing to file: {e}")

# def extract_rating(response_text):
#     # Search for a numeric rating pattern in the response text
#     match = re.search(r'\b\d+(\.\d+)?/10\b', response_text)
#     if match:
#         rating = float(match.group(0).split('/')[0])
#         if 0 <= rating <= 10:
#             return rating
#     return None

# # # Dummy technical question and user's answer
# # technical_question = "Explain the concept of object-oriented programming."
# # user_answer = "Object-oriented programming involves using objects and classes for coding."

# # # Path to the output file
# # output_file = "gemini_output.txt"

# # # Rate the user's answer and write the output to the specified file
# # rate_answer(technical_question, user_answer, output_file)

# # # Display a message indicating that the rating and/or suggestion has been written to the file
# # print("Rating and/or suggestion has been written to the file.")






import re

# Set your Gemini API key here
YOUR_API_KEY = "AIzaSyDKIARUcsy7sU9o5gkmFgg50YX-nY21Thg"

def rate_answer(question, user_answer, output_file):
    import google.generativeai as genai  # Import inside the function to avoid circular import

    # Configure the Gemini API with your API key
    genai.configure(api_key=YOUR_API_KEY)

    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-pro')

    # Generate a prompt by combining the question and user's answer
    prompt = f"Question: {question}\nAnswer: {user_answer}\n Rate the correctness of the answer out of 10."

    # Generate content using the prompt
    response = model.generate_content(prompt)

    # Extract the rating from the response
    rating = extract_rating(response.text)

    # Write the rating to the output file if rating is 7 or greater
    if rating is not None and rating >= 7:
        try:
            with open(output_file, 'w') as f:
                f.write(f"Rating: {rating}/10\n")
        except OSError as e:
            print(f"Error writing to file: {e}")
    else:
        # Write the Gemini model's response to the output file along with the rating if it's less than 7
        try:
            with open(output_file, 'w') as f:
                f.write("Suggestion:\n")
                f.write(response.text)
        except OSError as e:
            print(f"Error writing to file: {e}")

def extract_rating(response_text):
    # Search for a numeric rating pattern in the response text
    match = re.search(r'\b\d+(\.\d+)?/10\b', response_text)
    if match:
        rating = float(match.group(0).split('/')[0])
        if 0 <= rating <= 10:
            return rating
    return None

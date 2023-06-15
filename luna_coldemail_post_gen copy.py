import os
import csv
import openai

# Set your GPT-4 API key
openai.api_key = "Add you OpenAI Key here"

def generate_text(prompt, model="gpt-3.5-turbo-16k"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a witty assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

def count_files(folder_path):
    return len([file for file in os.listdir(folder_path) if file.endswith('.txt')])

def process_files():
    # Ask for the folder path from the user
    folder_path = input("Enter the folder path: ")

    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please try again.")
        return

    num_files = count_files(folder_path)
    print(generate_text(f"Hey, I found {num_files} files in the folder. I'm gonna start working on them."))

    progress_updates = [1, 5, 10]
    processed_files = 0

    # Create the CSV file
    with open(os.path.join(folder_path, "results.csv"), "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["File Name", "Post", "Email"])

        # Read text files in the folder
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as txt_file:
                    file_content = txt_file.read()

                    # Generate a post and a cold email using GPT-4.0-turbo
                    post_prompt = f"Generate a blog post based on the following text: {file_content}"
                    email_prompt = f"Generate a cold sales email based on the following text: {file_content}"

                    post = generate_text(post_prompt)
                    email = generate_text(email_prompt)

                    # Write the results to the CSV file
                    csv_writer.writerow([file_name, post, email])
                    processed_files += 1

                    if processed_files in progress_updates:
                        print(generate_text(f"I've processed {processed_files} files so far."))
      
    print(generate_text(f"Done processing {processed_files} files. Results saved to results.csv."))

# Example usage
process_files()
# ObsidianSpyder

## Overview
ObsidianSpyder is a program that helps the user research new topics. After receiving a research topic from the user, the program sends multiple queries to the OpenAI API in order to 'learn' about the specified topic. The program then formats and displays this information in a easy-to-read format (needs to be opened in the Obsidian note-taking app). In the example given, I have told the program to research Unity Trust Bank.

![Screenshot of output](https://i.imgur.com/c4x3wNG.png)

## Features
- **Automated Content Generation**: Leverages OpenAI's ChatCompletion to create detailed summaries and introductions on specified topics.
- **Bullet Points Generation**: Automatically generates a list of key subtopics for further exploration.
- **Content Expansion**: Expands on given bullet points for a more in-depth analysis.
- **Canvas Preparation**: Organises the generated content into a structured format suitable for visual presentation.

## Requirements
- Python 3.x
- `openai` Python package
- An active OpenAI API key

## Setup
1. Ensure Python 3 is installed on your system.
2. Install the `openai` package using pip. Ensure that it is version 0.28 as this is the version that ObsidianSpyder works with:
   ```bash
   pip install openai==0.28
   ```
3. Insert your OpenAI API key in the script by replacing the placeholder in `openai.api_key = ("********")` with your actual API key.

## Usage
1. Modify the `topic` variable at the beginning of the `if __name__ == "__main__":` block to your topic of interest.
2. Run the script:
   ```bash
   python main.py
   ```
3. The program will generate a `.canvas` file and a `bulletpoints.txt` file in the `Output` directory. These files contain the structured knowledge canvas and the bullet points for the topic, respectively.
4. Open the new .canvas file in Obsidian to view the result.

## Functionality Breakdown
- `generate_openai_response()`: Calls OpenAI API to generate responses based on the provided prompts.
- `calculate_node_height()`: Calculates the visual height of a node in the canvas based on the content length.
- `generate_bullet_points()`: Generates a list of bullet points for initial research on the topic.
- `generate_content()`: Creates detailed content for each subtopic identified.
- `write_to_file()`: Writes content to a specified file path.
- `generate_random_id()`: Generates a random hexadecimal ID for uniquely identifying canvas elements.
- `generate_introduction()`: Generates an introduction for the specified topic.
- `generate_overview()`: Creates an overview paragraph by summarising the generated bullet points.
- `generate_expanded_content()`: Expands on the initial content to provide a more thorough exploration of the topic.
- `stage1()`: Orchestrates the entire process, from generating bullet points to organising the final canvas structure. Potentially adding a Stage2 down the line.

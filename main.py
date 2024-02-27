import openai
import time
import secrets
import json

openai.api_key = ("********")


def generate_openai_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=3111
    )
    return response['choices'][0]['message']['content']


def calculate_node_height(content):
    content_lines = content.split('\n')
    lines_count = len(content_lines)
    return max(780 + (lines_count - 1) * 25, 780)


def generate_bullet_points(topic, system_message):
    prompt = (f"for the following topic, create a list of the main, most relevant and interesting topics in relation "
              f"to researching the topic and expanding knowledge on it. only output a bullet point list with no "
              f"additional details or expansion on each point. 8 topics. the topic is {topic}")
    messages = [system_message, {"role": "user", "content": prompt}]
    return generate_openai_response(messages)


def generate_content(topic, subtopic, system_message):
    prompt = (f"for the following subtopic, write a scientific, logical, well-sourced, intelligent summary of the "
              f"subtopic in relation to the topic, 1 paragraph max but heavily detailed. Only output the text with no "
              f"additional details or response. the topic is {topic} and the subtopic is {subtopic}.")
    messages = [system_message, {"role": "user", "content": prompt}]
    content = generate_openai_response(messages).replace('\n', '\\n')
    content = content.replace('"', '\\"')
    return content.replace('\\n', '\n')


def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def generate_random_id():
    return secrets.token_hex(8)


def generate_introduction(system_message):
    messages = [system_message, {"role": "user",
                                 "content": f'create an introduction to the topic of {topic}. be clear yet extremely '
                                            f'brief. 5 sentences max'}]
    result = generate_openai_response(messages)
    introduction_content = f"## Introduction to {topic}\n\n### {result}"

    node_data = {
        "id": "introduction_node",
        "type": "text",
        "text": introduction_content,
        "x": -1000,
        "y": -50,
        "width": 1180,
        "height": 330
    }

    return node_data


def generate_overview(topic, bullet_points, system_message):
    overview_content = f"## Overview\n\n{generate_content('take the following topics, and combine them all to make a new paragraph that is a summary of all of them, 5 short-ish sentences max', bullet_points, system_message)}"
    return overview_content


def generate_expanded_content(initial_content, system_message, expansion_level=1):
    prompt = f"expand on the following content:\n{initial_content}"
    messages = [system_message, {"role": "user", "content": prompt}]

    for _ in range(expansion_level):
        expanded_content = generate_openai_response(messages).replace('\n', '\\n')
        expanded_content = expanded_content.replace('"', '\\"')
        messages.append({"role": "user", "content": expanded_content})

    return expanded_content.replace('\\n', '\n')


def stage1():
    file_name = f"Output/{topic.replace(' ', '')}.canvas"
    write_to_file(file_name, "")

    canvas_id, topic_id, edge_id = "1a87034da1b26da0", "a3b5fcee5d904962", "c8d704708faea5bc"

    system_message = {
        "role": "system",
        "content": "As a versatile expert, I bring professionalism, intelligence, and wit "
                   "to every discussion. My unparalleled ability to synthesize "
                   "information spans philosophy, psychology, business, economics, "
                   "and health. Drawing inspiration from both ancient philosophers and "
                   "modern critical thinkers, I employ a complex yet effective strategy. "
                   "In decision-making, I leverage a holistic understanding where "
                   "economic principles, ethical considerations, and long-term vision "
                   "converge. With a commitment to accuracy, I use intricate language to "
                   "teach, drawing insights from diverse sources."
    }

    introduction_node = generate_introduction(system_message)

    bullet_points = generate_bullet_points(topic, system_message)
    write_to_file("bulletpoints.txt", bullet_points)

    modified_bullet_points = [line.replace('- ', '').strip() for line in bullet_points.split('\n')]

    overview_paragraph = generate_overview(bullet_points, '\n'.join(modified_bullet_points), system_message)

    nodes = [
        {"id": canvas_id, "type": "text", "text": f"# {topic}", "x": 220, "y": -50, "width": 300, "height": 329},
        {"id": "overview_node", "type": "text", "text": f"{overview_paragraph}", "x": 560, "y": -50, "width": 960,
         "height": 330},
        introduction_node
    ]

    x_offsets = [-360, 280, 920, -1000, -360, 280, 920, -1000]
    y_offsets = [320, 320, 320, -680, -680, -680, -680, 320]

    for idx, (subtopic, x_offset, y_offset) in enumerate(zip(modified_bullet_points, x_offsets, y_offsets), start=1):
        node_id = f"node_{idx}_{generate_random_id()}"
        content = generate_content(topic, subtopic, system_message)
        node_height = calculate_node_height(content)

        x_coordinate = x_offset * 1
        y_coordinate = y_offset * 1

        node_data = {
            "id": node_id,
            "type": "text",
            "text": f"## {subtopic.title()}\n{content}",
            "x": x_coordinate,
            "y": y_coordinate,
            "width": 600,
            "height": 600
        }
        nodes.append(node_data)

    graph_data = {
        "nodes": nodes
    }

    json_data = json.dumps(graph_data, indent=4)
    write_to_file(file_name, json_data)
    return json_data, modified_bullet_points


if __name__ == "__main__":
    topic = "Unity Trust Bank"
    s1, bullet_points = stage1()

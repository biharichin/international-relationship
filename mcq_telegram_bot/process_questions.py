import json
import re
import argparse
import os

def parse_questions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    questions = []
    current_question = {}
    question_number = 1

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('Answer:'):
            if 'question' in current_question and 'options' in current_question and len(current_question['options']) == 4:
                match = re.search(r'Answer: ([A-D])\)', line)
                if match:
                    correct_letter = match.group(1)
                    current_question['correct_option_index'] = ord(correct_letter) - ord('A')
                    current_question['question_number'] = question_number
                    questions.append(current_question)
                    question_number += 1
            current_question = {}
        elif line.startswith(('A)', 'B)', 'C)', 'D)')):
            if 'options' not in current_question:
                current_question['options'] = []
            current_question['options'].append(line[3:])
        else:
            if 'question' not in current_question:
                current_question['question'] = line
            # This handles cases where the question text might have multiple lines,
            # though the provided format seems to have single-line questions.
            # else:
            #     current_question['question'] += '\n' + line

    return questions

def main():
    parser = argparse.ArgumentParser(description='Parse MCQ questions from a text file.')
    parser.add_argument('input_file', help='The path to the input text file.')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'questions.json')
    
    parsed_questions = parse_questions(args.input_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_questions, f, indent=4)
        
    print(f"Successfully parsed {len(parsed_questions)} questions and saved to {output_file}")

if __name__ == '__main__':
    main()

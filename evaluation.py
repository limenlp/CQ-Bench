import argparse
import json
import os
import re
from sklearn.metrics import accuracy_score, f1_score
options_dict = {
    "not frequently":"not at all frequently",
    "not at all frequently":"not frequently",
    "not at all often":"not often",
    "not often":"not at all often",
    "very frequently":"quite frequently",
    "quite frequently":"very frequently",
    "definitely should have the right":"probably should have the right",
    "probably should have the right":"definitely should have the right",
    "definitely should not have the right":"probably should not have the right",
    "probably should not have the right":"definitely should not have the right",
}
def retrieve_predictions(options, numbers):
    
    predictions = []
    for number in numbers:
        if number>0 and number<=15:
            predictions.append(options[number-1])
    return '\n'.join(predictions)


def retrieve_number(result):
    return int(re.findall(r'\d+', result)[0])

# from calculate_statistics import match_value
def process_prediction(predictions, setting,options, if_reasoning,number_check=True):
    cnt = 0
    if setting == "1":
        if not if_reasoning:
            processed_predictions = [
                prediction.strip().strip("'").lower() for prediction in predictions
            ]

        else:
            processed_predictions = []
            for prediction in predictions:
                if "[Answer]" in prediction:
                    processed_predictions.append(
                        prediction.split("[Answer]")[1].strip().lower()
                    )
                    cnt+=1
                elif "**Answer**" in prediction:
                    processed_predictions.append(
                        prediction.split("**Answer**")[1].strip().lower()
                    )
                    cnt+=1
                elif "</think>" in prediction:
                    processed_predictions.append(
                        prediction.split("</think>")[1].strip().lower()
                    )
                    cnt+=1

                    
                else:
                    processed_predictions.append("")
                    # TODO: process corner cases

    elif setting == "2":
        if not if_reasoning:
            processed_predictions = [prediction.strip() for prediction in predictions]
        else:
            processed_predictions = []
            for prediction,option in zip(predictions,options):
                if "final answer" not in prediction.lower():
                    if "</think>" in prediction:
                        
                        retrieve_numbers= re.findall(r'\d+', prediction)
                        if len(retrieve_numbers)>0:
                            numbers = [int(number) for number in retrieve_numbers]
                            processed_predictions.append(retrieve_predictions(option,numbers))
                        else:
                            processed_predictions.append(
                            prediction.split("</think>")[1].strip().lower()
                            )
                    else:
                        processed_predictions.append('')
                else:
                    prediction=prediction.lower().split("final answer")[1]
                    retrieve_numbers= re.findall(r'\d+', prediction)
                    if len(retrieve_numbers)>0 and number_check:
                            numbers = [int(number) for number in retrieve_numbers]
                            processed_predictions.append(retrieve_predictions(option,numbers))
                    else:
                            processed_predictions.append(
                                prediction
                            )
                cnt += 1

    print("coverage = ", cnt / len(predictions))
    return processed_predictions


def longest_common_substrings(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    longest, substrings = 0, set()

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > longest:
                    longest = dp[i][j]
                    substrings = {s1[i - longest : i]}
                elif dp[i][j] == longest:
                    substrings.add(s1[i - longest : i])

    return list(substrings)


def match_value(value, ground_truth,setting):
    max_len = 0
    return_result = ""
    # ground_truth=ground_truth.split('\n')
    for gt in ground_truth:
        match_result = longest_common_substrings(value.lower(), gt.lower())
        if len(match_result) == 0:
            continue
        if len(match_result[0]) > max_len:
            max_len = len(match_result[0])
            return_result = gt
    if return_result!='':
        if setting == '1':
            # max_len>15:
            return return_result
        else:
            if max_len>15:
                return return_result
            else:
                return value
    else:
        return value


def compare_prediction_and_gold(predictions, gold_labels, setting, options=None):

    if setting == "1":
        # TODO: change f1 score
        acc_results = []
        matched_predictions = []
        # tp=0
        # fp=0
        # fn=0
        for prediction, option in zip(predictions, options):
            # option.remove(' neither agree or disagree ')
            prediction=prediction.strip(':').strip()
           
            matched_predictions.append(match_value(prediction, option,setting))
            
        matched_predictions = [
            prediction.strip().lower() for prediction in matched_predictions
        ]
        for prediction, gold_label in zip(matched_predictions, gold_labels):
            if prediction == gold_label:
                acc_results.append(1)
            else:
                # if gold_label in options_dict and options_dict[gold_label]==prediction:
                #     acc_results.append(1)
                # else:
                    acc_results.append(0)
        return acc_results
        # f1_score_return = f1_score(matched_predictions, gold_labels)
        # return f1_score_return
    elif setting == "2":
        precisions = []
        recalls = []
        f1_scores = []
        for prediction, ground_truth, option in zip(predictions, gold_labels, options):
            tp = 0
            fp = 0
            fn = 0
            if ground_truth == []:
                continue
            predicted_values = prediction.split("\n")
            matched_values = []
            if prediction == "":
                precisions.append(0)
                recalls.append(0)
                f1_scores.append(0)
                continue

            for predicted_value in predicted_values:

                if predicted_value.strip() == "":
                    # print("no predicted_value", predicted_values)
                    continue
                if "--" not in predicted_value or "--" not in predicted_value:
                    # print("no --")
                    matched_values.append("")
                    continue
                # if "--" not in predicted_value:
                #     
                #     continue
                matched_values.append(match_value(predicted_value, option,setting))
            # remove depulicate
            matched_values = list(set(matched_values))
            if matched_values == [""]:
                # print("no macthed_values")
                continue
            for value in matched_values:
                if value == "":
                    # print("empty value")
                    continue
                if value in ground_truth:
                    tp += 1
                else:
                    fp += 1
            for gt in ground_truth:
                if gt not in matched_values:
                    fn += 1
            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            if precision == 0 and recall == 0:
                f1_score = 0
            else:
                f1_score = 2 * precision * recall / (precision + recall)
            precisions.append(precision)
            recalls.append(recall)
            f1_scores.append(f1_score)

        return precisions, recalls, f1_scores


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Culture",
    )
    parser.add_argument(
        "--model",
        default="Qwen/Qwen2.5-7B-Instruct",
        choices=[
            "Qwen/Qwen2.5-7B-Instruct",
            "Qwen/Qwen2.5-14B-Instruct",
            "Qwen/Qwen2.5-32B-Instruct",
            
            "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
            "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
            "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
            "Llama-3.1-8B-Instruct",
            "llama3.1_sft",
            "llama3.1_ft_task_1"
            "meta-llama/Llama-3.2-3B-Instruct",
            "gpt-4o-mini",
            "o3-mini",
            "o1"
        ],
    )
    parser.add_argument("--setting", default="1", choices=["1", "2", "3"])
    parser.add_argument(
        "--category",
        default="social",
        choices=["random", "politic", "ethical", "religious", "social", "multiple",'human'],
    )
    parser.add_argument('-p','--prompt',default='zero', choices=['zero','one'])
    
    parser.add_argument("-r", "--reasoning", action="store_true")
    args = parser.parse_args()
    f = open("evaluate_results.txt", "a")
    result_folder = os.path.join("results", args.model)
    reasoning = args.reasoning
    setting = args.setting
    category = args.category
    prompt_type = args.prompt
    if args.reasoning:
        if 'sft' not in args.model:
            if prompt_type == 'one':
                output_file = f'results_{setting}_{category}_reasoning_one_shot.json'
            else:
                output_file = f'results_{setting}_{category}_reasoning.json'
        else:
            output_file = f'results_{setting}_{category}_reasoning_sft.json'
    else:
        output_file = f'results_{setting}_{category}.json'
    print(output_file)
    prediction_file = os.path.join(result_folder, output_file)
    if args.category == "random":
        dataset_file = f"dataset_setting{setting}_random.json"
    else:
        dataset_file = f"dataset_setting{setting}_{category}.json"

    predictions = json.load(open(prediction_file))
    dataset = json.load(open(os.path.join("datasets", dataset_file)))
    metric_file = "metric_" + output_file
    if args.setting == "1":
        gold_labels = []
        options = []
        for datapoint in dataset:
            for question in datapoint["questions"]:
                # if question['gold label']=="neither agree or disagree":
                #     continue
                gold_labels.append(question["gold label"].lower())
                
                options.append(question["options"])

        predictions_processed = process_prediction(predictions, args.setting,options, reasoning)
        results = compare_prediction_and_gold(
            predictions_processed, gold_labels, setting, options
        )

        json.dump(results, open(os.path.join(result_folder, metric_file), "w"))
        acc_score = sum(results) / len(results)
        f.write(
            f"Setting:{setting},category:{category},if_reasoning:{reasoning},model:{args.model},type:{args.prompt}\n"
        )
       
        f.write(f"acc:{acc_score}\n")
        print(f"acc:{acc_score}\n")
        f.write("---------------------------\n")
        f.close()
    elif args.setting == "2":
        gold_labels = [datapoint["values"] for datapoint in dataset]
        options = [datapoint["options"] for datapoint in dataset]
        predictions_processed = process_prediction(predictions, setting, options, reasoning)
        precision_results, recall_results, f1_score_results = (
            compare_prediction_and_gold(
                predictions_processed, gold_labels, setting, options
            )
        )
        precision = sum(precision_results) / len(precision_results)
        recall = sum(recall_results) / len(recall_results)
        f1_score = 2 * precision * recall / (precision + recall)
        json.dump(f1_score_results, open(os.path.join(result_folder, metric_file), "w"))
        f.write(
            f"Setting:{setting},category:{category},if_reasoning:{reasoning},model:{args.model}, type:{args.prompt}\n"
        )
        print( f"Setting:{setting},category:{category},if_reasoning:{reasoning},model:{args.model}, type:{args.prompt}\n"
    )
        f.write(f"f1:{f1_score}\n")
        print(f"f1:{f1_score}\n")
        f.write("---------------------------\n")
        f.close()

# GPTUsageStatistics
# 出5000刀组织/官方直连额度 微信kaqijiang
# 手动去官方下载使用情况json。放到同文件夹下。命名data.json
# 价格不准的话更新模型价格。

import json

# 文件路径
file_path = './data11.json'

model_costs = {
    "gpt-3.5-turbo-0613": {"context": 0.001, "generated": 0.002},
    'gpt-3.5-turbo-1106': {'context': 0.001, 'generated': 0.002},
    "gpt-3.5-turbo-16k-0613": {"context": 0.001, "generated": 0.002},
    'gpt-3.5-turbo-instruct': {'context': 0.0015, 'generated': 0.002},
    'gpt-3.5-turbo': {'context': 0.003, 'generated': 0.006},
    "gpt-4-0314": {"context": 0.03, "generated": 0.06},
    "gpt-4-0613": {"context": 0.03, "generated": 0.06},
    'gpt-4': {'context': 0.03, 'generated': 0.06},
    'gpt-4-32k': {'context': 0.06, 'generated': 0.12},
    'gpt-4-1106-preview': {'context': 0.01, 'generated': 0.03},
    'gpt-4-1106-vision-preview': {'context': 0.01, 'generated': 0.03},
    'davinci-002': {'context': 0.012, 'generated': 0.012},
    'babbage-002': {'context': 0.0016, 'generated': 0.0016},
    'text-embedding-ada-002-v2': {'context': 0.06, 'generated': 0.06},
    'dalle': {'256x256': 0.016, '512x512': 0.018, '1024x1024': 0.04},
    'whisper-1': {'context': 0.006 / 60, 'generated': 0}
}


# 计算每个用户和模型的成本的函数
def calculate_user_model_costs(data, model_costs):
    user_costs = {}
    model_total_costs = {}  # 用于存储每个模型的总金额
    for record in data["data"]:
        user = record["user"]
        # 根据使用类型计算成本
        usage_type = record.get("usage_type")
        model = record.get("model",usage_type)


        if usage_type == "text":
            context_tokens = record.get("n_context_tokens_total", 0)
            generated_tokens = record.get("n_generated_tokens_total", 0)
            cost = (context_tokens * model_costs.get(model, {}).get('context', 0) / 1000) + \
                   (generated_tokens * model_costs.get(model, {}).get('generated', 0) / 1000)
        elif usage_type == "dalle":
            image_size = record.get("image_size")
            num_images = record.get("num_images", 0)
            cost_per_image = model_costs.get('dalle', {}).get(image_size, 0.0)
            cost = cost_per_image * num_images
        elif usage_type == "asr":
            num_seconds = record.get("num_seconds", 0)
            cost = num_seconds * model_costs.get(model, {}).get('context', 0)
        else:
            cost = 0

        # 更新模型总金额
        model_total_costs[model] = model_total_costs.get(model, 0) + cost

        # 累计用户成本
        if user not in user_costs:
            user_costs[user] = {'total_cost': 0, 'models': {}}
        user_costs[user]['total_cost'] += cost
        if model in user_costs[user]['models']:
            user_costs[user]['models'][model] += cost
        else:
            user_costs[user]['models'][model] = cost

    return user_costs, model_total_costs



# 从文件读取JSON数据的函数
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# 从文件读取数据
data_from_file = read_json_file(file_path)

# 计算成本
user_model_costs, model_total_costs = calculate_user_model_costs(data_from_file, model_costs)

total_cost_for_all_users = 0

for user, costs in user_model_costs.items():
    print()
    print(f"用户: {user}")
    print(f"总费用: {costs['total_cost']:.2f} 美元")
    for model, model_cost in costs['models'].items():
        print(f"  - Model {model}: {model_cost:.2f} 美元")
    total_cost_for_all_users += costs['total_cost']

# 所有用户的总费用
print(f"\n所有用户的总费用: {total_cost_for_all_users:.2f} 美元")
for model, total_cost in model_total_costs.items():
    print(f"  - Model {model}: {total_cost:.2f} 美元")

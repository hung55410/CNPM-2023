import tkinter as tk;
from tkinter import messagebox;
from tkinter import ttk;
from collections import Counter;
from math import log;

# Du lieu huan luyen
training_data = [
    {'Quang cảnh': 'Nắng', 'Nhiệt độ': 'Nóng', 'Độ ẩm': 'Cao', 'Gió': 'Nhẹ', 'Chơi': 'Không'},
    {'Quang cảnh': 'Nắng', 'Nhiệt độ': 'Nóng', 'Độ ẩm': 'Cao', 'Gió': 'Mạnh', 'Chơi': 'Không'},
    {'Quang cảnh': 'Âm u', 'Nhiệt độ': 'Nóng', 'Độ ẩm': 'Cao', 'Gió': 'Nhẹ', 'Chơi': 'Có'},
    {'Quang cảnh': 'Mưa', 'Nhiệt độ': 'Ấm áp', 'Độ ẩm': 'Cao', 'Gió': 'Nhẹ', 'Chơi': 'Có'},
    {'Quang cảnh': 'Mưa', 'Nhiệt độ': 'Mát', 'Độ ẩm': 'Trung bình', 'Gió': 'Nhẹ', 'Chơi': 'Có'},
    {'Quang cảnh': 'Mưa', 'Nhiệt độ': 'Mát', 'Độ ẩm': 'Trung bình', 'Gió': 'Mạnh', 'Chơi': 'Không'},
    {'Quang cảnh': 'Âm u', 'Nhiệt độ': 'Mát', 'Độ ẩm': 'Trung bình', 'Gió': 'Mạnh', 'Chơi': 'Có'},
    {'Quang cảnh': 'Nắng', 'Nhiệt độ': 'Ấm áp', 'Độ ẩm': 'Cao', 'Gió': 'Nhẹ', 'Chơi': 'Không'},
    {'Quang cảnh': 'Nắng', 'Nhiệt độ': 'Mát', 'Độ ẩm': 'Trung bình', 'Gió': 'Nhẹ', 'Chơi': 'Có'},
    {'Quang cảnh': 'Mưa', 'Nhiệt độ': 'Ấm áp', 'Độ ẩm': 'Trung bình', 'Gió': 'Nhẹ', 'Chơi': 'Có'},
    {'Quang cảnh': 'Nắng', 'Nhiệt độ': 'Ấm áp', 'Độ ẩm': 'Trung bình', 'Gió': 'Mạnh', 'Chơi': 'Có'},
    {'Quang cảnh': 'Âm u', 'Nhiệt độ': 'Ấm áp', 'Độ ẩm': 'Cao', 'Gió': 'Mạnh', 'Chơi': 'Có'},
    {'Quang cảnh': 'Âm u', 'Nhiệt độ': 'Nóng', 'Độ ẩm': 'Trung bình', 'Gió': 'Nhẹ', 'Chơi': 'Có'},
    {'Quang cảnh': 'Mưa', 'Nhiệt độ': 'Ấm áp', 'Độ ẩm': 'Cao', 'Gió': 'Mạnh', 'Chơi': 'Không'}
]

def entropy(data):
    class_labels = [record['Chơi']for record in data]
    class_counts = Counter(class_labels)
    num_record = len(data)
    
    entropy = 0
    for count in class_counts.values():
        probality = count / num_record
        entropy -= probality * log(probality, 2)
        
    return entropy

def information_gain(data, attribute):
    attribute_values = set(record[attribute] for record in data)
    num_records = len(data)
    subset_entropy = 0
    
    for value in attribute_values:
        subset = [record for record in data if record[attribute] == value]
        subset_probality = len(subset) / num_records;
        subset_entropy += subset_probality * entropy(subset)
        
    return entropy(data) - subset_entropy

def build_tree(data, attributes, taget_attribute):
    class_labels = [record[taget_attribute] for record in data]
    
    if len(set(class_labels)) == 1:
        return class_labels[0]
    
    if len(attributes) == 0:
        majority_label = Counter(class_labels).most_common(1)[0][0]
        return majority_label
    
    best_attribute = max(attributes, key = lambda attr: information_gain(data, attr))
    
    tree = {best_attribute: {}}
    remaining_attibutes = attributes - {best_attribute}
    
    for value in set(record[best_attribute] for record in data):
        subset = [record for record in data if record[best_attribute] == value]
        subtree = build_tree(subset, remaining_attibutes, taget_attribute)
        tree[best_attribute][value] = subtree
        
    return tree

def classify(record, tree):
    if isinstance(tree, dict):
        attribute = next(iter(tree))
        value = record.get(attribute)
        if value is None:
            # Handle missing attribute in the record
            return "Unknown"
        
        subtree = tree[attribute].get(value)
        
        if subtree is None:
            # Handle cases where the attribute value is not in the tree
            return "Unknown"
        
        return classify(record, subtree)
    else:
        return tree

def get_decision(record, tree):
    decision = classify(record, tree)
    if decision is None:
        return 'Unknown'
    return decision

def on_predict():
    record = {
        'Quang cảnh': combo_quangcanh.get(),
        'Nhiệt độ': combo_nhietdo.get(),
        'Độ ẩm': combo_doam.get(),
        'Gió': combo_gio.get()
    }
    decision = get_decision(record, tree)
    result_label.configure(text=f"Chơi: {decision}")
    if decision == 'Có':
        result_label.configure(foreground="green")
    elif decision == 'Không':
        result_label.configure(foreground="red")
    else:
        result_label.configure(foreground="black")
        
        
# Tạo giao diện Tkinter
root = tk.Tk()
root.title("ID3 Decision Tree")

# Tạo frame chứa phần nhập liệu và phần kết quả
input_frame = ttk.Frame(root, padding=20)
input_frame.grid(row=0, column=0, padx=20, pady=10)
result_frame = ttk.Frame(root, padding=20)
result_frame.grid(row=1, column=0, padx=20, pady=10)

# Label và combobox cho từng thuộc tính
label_quangcanh = ttk.Label(input_frame, text="Quang cảnh:")
label_quangcanh.grid(row=0, column=0, sticky="W", padx=5, pady=5)
combo_quangcanh = ttk.Combobox(input_frame, values=['Nắng', 'Âm u', 'Mưa'])
combo_quangcanh.grid(row=0, column=1, padx=5, pady=5)
label_nhietdo = ttk.Label(input_frame, text="Nhiệt độ:")
label_nhietdo.grid(row=1, column=0, sticky="W", padx=5, pady=5)
combo_nhietdo = ttk.Combobox(input_frame, values=['Nóng', 'Ấm áp', 'Mát'])
combo_nhietdo.grid(row=1, column=1, padx=5, pady=5)
label_doam = ttk.Label(input_frame, text="Độ ẩm:")
label_doam.grid(row=2, column=0, sticky="W", padx=5, pady=5)
combo_doam = ttk.Combobox(input_frame, values=['Cao', 'Trung bình'])
combo_doam.grid(row=2, column=1, padx=5, pady=5)
label_gio = ttk.Label(input_frame, text="Gió:")
label_gio.grid(row=3, column=0, sticky="W", padx=5, pady=5)
combo_gio = ttk.Combobox(input_frame, values=['Nhẹ', 'Mạnh'])
combo_gio.grid(row=3, column=1, padx=5, pady=5)

# Button "Dự đoán"
button_predict = ttk.Button(input_frame, text="Dự đoán", command=on_predict)
button_predict.grid(row=4, columnspan=2, pady=10)
# Label hiển thị kết quả

result_label = ttk.Label(result_frame, text="Chơi: ")
result_label.pack()
# Xây dựng cây quyết định ID3

attributes = {'Quang cảnh', 'Nhiệt độ', 'Độ ẩm', 'Gió'}
tree = build_tree(training_data, attributes, 'Chơi')
root.mainloop()
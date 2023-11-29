
import csv
import numpy as np
import math

#Đọc dữ liệu từ tập tin CSV, loại bỏ hàng đầu tiên và cột đầu tiên, sau đó trộn ngẫu nhiên dữ liệu và chia thành tập huấn luyện và tập kiểm tra theo tỉ lệ 100:50.
def loadData(path):
    f = open(path, "r")
    data = csv.reader(f)
    data = np.array(list(data))
    data = np.delete(data, 0, 0)
    data = np.delete(data, 0, 1)
    np.random.shuffle(data)
    f.close()
    trainSet = data[:100]
    testSet = data[100:]
    return trainSet, testSet

#Tính toán khoảng cách Euclid giữa hai điểm dữ liệu.
def calcDistancs(pointA, pointB, numOfFeature=4):
    tmp = 0
    for i in range(numOfFeature):
        tmp += (float(pointA[i]) - float(pointB[i])) ** 2
    return math.sqrt(tmp)

#Tính toán khoảng cách giữa điểm dữ liệu cần dự đoán và tất cả các điểm trong tập huấn luyện, sau đó chọn ra k láng giềng gần nhất.
def kNearestNeighbor(trainSet, point, k):
    distances = []
    for item in trainSet:
        distances.append({
            "label": item[-1],
            "value": calcDistancs(item, point)
        })
    distances.sort(key=lambda x: x["value"])
    labels = [item["label"] for item in distances]
    return labels[:k]

# Tìm ra nhãn xuất hiện nhiều nhất trong danh sách.
def findMostOccur(arr):
    labels = set(arr)
    ans = ""
    maxOccur = 0
    for label in labels:
        num = arr.count(label)
        if num > maxOccur:
            maxOccur = num
            ans = label
    return ans

#Tải dữ liệu từ tập tin "Iris.csv", chia thành tập huấn luyện và tập kiểm tra.
#Duyệt qua từng mẫu trong tập kiểm tra, sử dụng thuật toán "k-nearest neighbor" để dự đoán nhãn, sau đó tính toán độ chính xác của thuật toán dựa trên số lượng dự đoán đúng.
#In ra tỉ lệ độ chính xác của thuật toán.
if __name__ == "__main__":
    trainSet, testSet = loadData("./Iris.csv")
    numOfRightAnwser = 0
    for item in testSet:
        knn = kNearestNeighbor(trainSet, item, 5)
        answer = findMostOccur(knn)
        numOfRightAnwser += item[-1] == answer
        print("label: {} -> predicted: {}".format(item[-1], answer))
    print("Accuracy", numOfRightAnwser/len(testSet))
import numpy as np
def get_dot(vec_a, vec_b):
    if len(vec_a) != len(vec_b):
        return ValueError("2个向量的维度必须数量相同")

    dot_sum = 0
    for a,b in zip(vec_a, vec_b):
        dot_sum += a*b
    return dot_sum

def get_norm(vec):
    sum_square = 0
    for v in vec:
        sum_square += v**2
    return np.sqrt(sum_square)

def cosine_similarity(vec_a, vec_b):
    result = get_dot(vec_a, vec_b)/(get_norm(vec_a)*get_norm(vec_b))
    print(result)

if __name__ == "__main__":
    vec_a = [0.5,0.5]
    vec_b = [0.4,0.4]
    cosine_similarity(vec_a, vec_b)

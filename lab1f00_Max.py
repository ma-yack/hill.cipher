import numpy as np

                                                                            #ENCODING 
print()
print("ЗАШИФРУВАННЯ ПОВІДОМЛЕННЯ")
print()

alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя ,.!"
plain_text = "зберігайте спокій! працюємо, переможемо.якимович"
print('Потужність алфавіту:' + str(len(plain_text)))
print('Вихідний текст:' + plain_text)
col_num = len(plain_text) // 3
plain_matrix = np.eye(3, col_num)
key = np.array([[3, 2, 3], # Determinant = 12
                [4, 5, 6],
                [1, 8, 9]])
counter = 0
for i in range(0, len(plain_text), 3):
    plain_matrix[0][counter] = alphabet.index(plain_text[i])
    plain_matrix[1][counter] = alphabet.index(plain_text[i + 1])
    plain_matrix[2][counter] = alphabet.index(plain_text[i + 2])
    counter += 1
counter = 0

encrypted_matrix = key.dot(plain_matrix) % len(alphabet)
encrypted_text = ""
for i in range(len(encrypted_matrix[0])):
    a = int(encrypted_matrix[0][i])
    b = int(encrypted_matrix[1][i])
    c = int(encrypted_matrix[2][i])
    encrypted_text = encrypted_text + alphabet[a]
    encrypted_text = encrypted_text + alphabet[b]
    encrypted_text = encrypted_text + alphabet[c]

print(f"Зашифований текст:{encrypted_text}") ; print()
                                                                            #DECODING 

def dete(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[2][1] * a[1][2])
           -a[1][0] * (a[0][1] * a[2][2] - a[2][1] * a[0][2])
           +a[2][0] * (a[0][1] * a[1][2] - a[1][1] * a[0][2]))

def find_inverse_matrix(matrix):
    resultMatrix = np.eye(3, 3)
    detMatrix = dete(matrix)
    invDet = modInverse(detMatrix, len(alphabet))
    resultMatrix[0][0] = 1 * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
    resultMatrix[0][1] = -1 * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
    resultMatrix[0][2] = 1 * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    resultMatrix[1][0] = -1 * (matrix[0][1] * matrix[2][2] - matrix[0][2] * matrix[2][1])
    resultMatrix[1][1] = 1 * (matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0])
    resultMatrix[1][2] = -1 * (matrix[0][0] * matrix[2][1] - matrix[0][1] * matrix[2][0])
    resultMatrix[2][0] = 1 * (matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1])
    resultMatrix[2][1] = -1 * (matrix[0][0] * matrix[1][2] - matrix[0][2] * matrix[1][0])
    resultMatrix[2][2] = 1 * (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])
    resultMatrix = resultMatrix.transpose()
    return resultMatrix * invDet

def modInverse(A, M):                                                       # Функція яка шукає обернений елемент
    for X in range(1, M):
        if (((A % M) * (X % M)) % M == 1):
            return X
    return -1

def find_last_piece(str):                                                   # Функція яка шукає останні 9 символів повідомлення
    result_martix_b = np.array([[0,0,0],
                                [0,0,0],
                                [0,0,0]])
    c = 2
    for i in range(0, 3, 1):
        for j in range(0, 3, 1):
            result_martix_b[(2-j)][(2-i)] = alphabet.index(str[(1 - c)])
            c = c+1
    return result_martix_b

print("КРИПТОАНАЛІЗ ПОВІДОМЛЕННЯ")
print()

cypher_text = "оддндєйо юхб!!иохнджайо ьххдґмєохшдфяєфрпхєлщігдвурцкь"
print(f"Отриманий шифр: {cypher_text}")


for k in range(0,len(alphabet)):
    col_num = len(cypher_text) // 3
    last_piece = np.array([[k,  15, 17],                                    #Кінець повідомлення у матричому вигляді
                           [21, 0,  10],
                           [0,  28, 14]])

    det_last_piece = dete(last_piece)
    last_piece_encrypted = find_last_piece(cypher_text)                     #Зашифрований кінець повідомлення в матричному вигляді:
    inverted_last_piece_matrix = find_inverse_matrix(last_piece)            #Транспонована матриця доповнень * обернений елемент визначника
                                                                            # = Оберернена матриця прізвища
    assumed_key = last_piece_encrypted.dot(inverted_last_piece_matrix) % 37 #Можливий ключ
    cypher_text_matrix = np.eye(3, col_num)
    for i in range(0, len(cypher_text), 3):
        cypher_text_matrix[0][counter] = alphabet.index(cypher_text[i])
        cypher_text_matrix[1][counter] = alphabet.index(cypher_text[i+1])
        cypher_text_matrix[2][counter] = alphabet.index(cypher_text[i+2])
        counter += 1
    counter = 0

    add_a_key_matrix = find_inverse_matrix(assumed_key)   
    result_arr = add_a_key_matrix.dot(cypher_text_matrix) % 37
    result_Message = " "
    for i in range(len(result_arr[0])):
        a = int(result_arr[0][i])
        b = int(result_arr[1][i])
        c = int(result_arr[2][i])
        result_Message = result_Message + alphabet[a]
        result_Message = result_Message + alphabet[b]
        result_Message = result_Message + alphabet[c]
    print()
    print(str(k) + ". Розшифроване повідомлення:" + str(result_Message))

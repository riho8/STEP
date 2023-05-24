# HW2 (5/19-)

## Explanation of the homework

1. Create hash table.
    1. implement delete() function
    2. improve calculate_hash() function
    3. implement rehash 
2. Explain why actual large databases adopt a tree structure rather than a hash table.
3. Consider a data structure that allows O(1) to manage the cache.

## hw2-1

### **How to Run**

```python
$ python3 hw2-1.py
```

The program includes tests to verify the behavior and performance of the hash table.

If the output shows "Functional tests passed!" and "Performance tests passed!", the program is successful.

### **Implement the delete() function**

The delete() function is implemented using the following steps:

1. Calculate the hash value.
2. Access the bucket that corresponds to the hash value and search for the target item.
3. If the target item is found, delete it.

Points:

- The deletion method differs depending on whether the item is at the head of the bucket or not.

### **Improve the calculate_hash() function**

The calculate_hash() function is improved using the following steps:

1. Multiply the current hash value by 97 and add the ASCII value of the current character.
2. Update the hash variable with the new calculated value.

Points:

- The multiplication by 97 and addition of the ASCII value of the character help create a unique hash value for each different key.
- 97 was chosen because it is the closest prime number from 94, which is the difference between the ASCII code range of 32 to 126, including commonly used printable characters.
- Performance: avg: 0.193112 SD: 0.583235 max: 5.226970 min: 0.065486

### **Implement rehashing**

The rehashing process is implemented using the following steps:

**`check_and_resize_table()`**

1. Check if the hash table needs to be resized.
    - If the table is too small (less than 30% used), the bucket size is halved.
    - If the table is too large (more than 70% used), the bucket size is doubled.

**`rehash()`**

1. Create a new hash table with the new bucket size.
2. Take out the elements from the old hash table one by one and reinsert them into the new hash table. The hash value is calculated based on the new size.
3. Switch to using the new hash table.

Points:

- The bucket size should be a prime number. To find a prime number, the **`nextprime()`** function from the **`sympy`** library is used.
    - Example: **`from sympy import nextprime`**

## [hw2-2](hw2-2.md)

## [hw2-3](hw2-3.md)
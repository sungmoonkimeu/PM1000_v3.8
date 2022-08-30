# Python3 program to demonstrate above steps
# of binary fractional to decimal conversion

# Function to convert binary fractional
# to decimal
def binaryToDecimal(binary, length):
    # Fetch the radix point
    point = binary.find('.')

    # Update point if not found
    if (point == -1):
        point = length

    intDecimal = 0
    fracDecimal = 0
    twos = 1

    # Convert integral part of binary
    # to decimal equivalent
    for i in range(point - 1, -1, -1):
        # Subtract '0' to convert
        # character into integer
        intDecimal += ((ord(binary[i]) -
                        ord('0')) * twos)
        twos *= 2

    # Convert fractional part of binary
    # to decimal equivalent
    twos = 2

    for i in range(point + 1, length):
        fracDecimal += ((ord(binary[i]) -
                         ord('0')) / twos);
        twos *= 2.0

    # Add both integral and fractional part
    ans = intDecimal + fracDecimal

    return ans


# Driver code :
if __name__ == "__main__":
    n = "110.101"
    print(binaryToDecimal(n, len(n)))

    n = "101.1101"
    print(binaryToDecimal(n, len(n)))

# This code is contributed
# by aishwarya.27
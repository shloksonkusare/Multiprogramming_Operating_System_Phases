m = 0
IR = [0 for i in range(4)]
IC = [0 for i in range(2)]
R = [0 for i in range(4)]
C = False
SI = 0

memory = [['_' for i in range(4)] for j in range(100)]
fout = open('output.txt', 'w')
buffer_id = []
data_index = 0

def PRINT_MEMORY():
    print("Contents of the external memory location: \n")
    for i in range(100):
        print(i, " ".join(memory[i]))
        if i % 10 == 9:
            print()
    print("\n\n")

def GET_DATA(address):
    global data_index
    i = 0
    j = 0
    line = buffer_id[data_index]
    address = (address// 10) * 10
    while line[i] != '\n' :
        memory[address][j] = line[i]
        i += 1
        j += 1
        if j == 4:
            j = 0
            address += 1
    data_index += 1
    PRINT_MEMORY()

def PUT_DATA(address):
    address = (address // 10) * 10
    for i in range(address, address + 10):
        for j in range(4):
            if memory[i][j] == '_':
                break
            print(memory[i][j], end="", file=fout)
    print(file = fout)

def HALT():
    print("\n", file=fout)

def LOAD():
    with open("input.txt", 'r') as file:
        global buffer_id
        buffer_id = file.readlines()
        counter = -1
        index = 0
        while index < len(buffer_id):
            global data_index
            line = buffer_id[index]
            if line[0].startswith('$'):
                if line[1:4] == 'AMJ':
                    global id, time, lines_printed
                    id = line[4:8]
                    time = line[8:12]
                    lines_printed = line[12:16]
                    counter = 0
                elif line[1:4] == 'DTA':
                    counter = 1
                    data_index = index + 1
                    START_EXECUTION()
                    index = data_index - 1
                elif line[1:4] == 'END':
                    counter = -1
                    global memory, C
                    C = False
                    memory = [['_' for i in range(4)] for j in range(100)]
                else:
                    print("ERROR IN INPUT")
                    exit(-1)

            else:
                if counter == 0:
                    i = 0
                    for m in range(int(time)):
                        if line[i] == 'H':
                            memory[m][0] = line[i]
                            i += 1
                        else:
                            memory[m][0:4] = line[i:i+4]
                            i += 4
            index += 1


def START_EXECUTION():
    IC[0] = 0
    IC[1] = 0
    EXECUTE_USER_PROGRAM()

def MOS():
    global SI
    if SI == 1:
        GET_DATA(int(IR[2]) * 10 + int(IR[3]))
    elif SI == 2:
        PUT_DATA(int(IR[2]) * 10 + int(IR[3]))
    elif SI == 3:
        HALT()

def EXECUTE_USER_PROGRAM():
    for i in range(int(time)):
        global IC, IR, R, C, T, SI
        IR = memory[10 * IC[0] + IC[1]]
        IC[1] += 1
        if IC[1] == 10:
            IC[0] += 1
            IC[1] = 0
        inst = "" + IR[0] + IR[1]

        if inst == "LR":
            R = memory[int(IR[2]) * 10 + int(IR[3])]
        elif inst == "SR":
            memory[int(IR[2]) * 10 + int(IR[3])] = R
        elif inst == "CR":
            if (memory[int(IR[2]) * 10 + int(IR[3])] == R):
                C = True
            else:
                C = False
        elif inst == "BT":
            if (C):
                IC[0] = int(IR[2])
                IC[1] = int(IR[3])
        elif inst == "GD":
            SI = 1
            MOS()
        elif inst == "PD":
            SI = 2
            MOS()
        elif inst == "H\0":
            SI = 3
            MOS()
            break

if __name__ == "__main__":
    LOAD()
    fout.close()

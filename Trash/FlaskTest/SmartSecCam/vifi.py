from wifi import Cell, Scheme

cells = Cell.all('wlp3s0')
for cell in cells:
    print('#############################')
    print(cell.ssid)
    print(cell.signal)
    print(cell.quality)
    print(cell.frequency)
    print(cell.bitrates)
    print(cell.encrypted)
    print(cell.channel)
    print(cell.address)
    print(cell.mode)

# i = 0

# while (cells[i]):
#     print('#############################')
#     print(cells[i].ssid)
#     print(cells[i].signal)
#     print(cells[i].quality)
#     print(cells[i].frequency)
#     print(cells[i].bitrates)
#     print(cells[i].encrypted)
#     print(cells[i].channel)
#     print(cells[i].address)
#     print(cells[i].mode)

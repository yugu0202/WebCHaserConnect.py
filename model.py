import random
import WebCHaserConnect

client = WebCHaserConnect.Client("test",host="localhost", port=4000, secure=False)
direction = 0
before_move = None

def move(direction):
  if direction == 2:
    client.walkUp()
  elif direction == 4:
    client.walkLeft()
  elif direction == 6:
    client.walkRight()
  elif direction == 8:
    client.walkDown()

# アイテムを見つけたら方向を記録する
def get_item(values):
    item = []
    for i in range(2, 10, 2):
        if values[i] == 3:
            item.append(i)

    return item

# 動ける方向を記録する
def able_move(values):
    can_move = get_item(values)
    if len(can_move) == 0:
        for i in range(2, 10, 2):
            if values[i] != 2:
                can_move.append(i)

    return can_move

#動ける方向の配列から方向を決定する
def decision_direction(can_move,before_move):
    if len(can_move) == 1:
        direction = can_move[0]
    elif before_move is None:
        direction = random.choice(can_move)
    else:
        #前回移動した方向に戻る方向へ変換する
        before_move_reverse = 10 - before_move
        #その方向を移動先リストから削除することで戻らないようにする
        if before_move_reverse in can_move:
            can_move.remove(before_move_reverse)
        direction = random.choice(can_move)

    return direction


while True:
  values = client.getReady()
  print(values)

  if values[0] == 0:
    break

  can_move = able_move(values)

  direction = decision_direction(can_move, before_move)
  move(direction)

  before_move = direction

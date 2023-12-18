import pyxel

pyxel.init(200,200)
pyxel.mouse(True)

start_x=0
start_y=0
end_x=0
end_y=0
button_count=0

def update():
    global start_x,start_y,end_x,end_y,button_count
    if button_count % 2 ==0:
        if pyxel.btnp(pyxel.KEY_SPACE):
            start_x = pyxel.mouse_x
            start_y = pyxel.mouse_y
            end_x = pyxel.mouse_x
            end_y = pyxel.mouse_y
            button_count += 1
    else:
        end_x = pyxel.mouse_x
        end_y = pyxel.mouse_y
        if pyxel.btnp(pyxel.KEY_SPACE):
            button_count += 1                

def draw():
    global start_x,start_y,end_x,end_y,button_count
    pyxel.cls(7)
    pyxel.line(start_x,start_y,end_x,end_y, 0)

pyxel.run(update, draw)
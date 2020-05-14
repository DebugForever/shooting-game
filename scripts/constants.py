"""
存放常量
contains constants used in program
"""

# 这些常量也可以用int类型，像c++风格的枚举一样，
# 也可以用python的enum类，但是用字符串会方便调试一些
PLAYER_BULLET_NAME = 'bullet1'
ENEMY_BULLET_NAME = 'bullet2'
CONTROL_MOUSE = 'mouse'
CONTROL_KEYBOARD = 'keyboard'
CONTROL_JOYSTICK = 'joystick'

# 按键相关
CONTROL_UP = 'up'
CONTROL_DOWN = 'down'
CONTROL_LEFT = 'left'
CONTROL_RIGHT = 'right'
CONTROL_FIRE = 'fire'
CONTROL_DEBUG = 'fps'

# 怪物ai状态相关
STATUS_TYPE = str
STATUS_IDLE = 'idle'  # 待机
STATUS_MOVE = 'move'  # 移动
STATUS_FIRE = 'fire'  # 射击

# 游戏进行状态相关
ACTIVE_START = 'start' # 弹出play按钮，这是整个游戏的开始界面
ACTIVE_PLAY = 'play' # 正常进行游戏，这个时候menu是需要存在的
ACTIVE_LIST = 'list' # 弹出list，这个时候游戏是需要暂停的
ACTIVE_QUIT = 'quit' # 退出游戏

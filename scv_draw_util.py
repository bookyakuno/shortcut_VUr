import gpu

from gpu_extras.batch import batch_for_shader

class SCV_Draw_Util:

    def __init__(self, context):
        self.x_off = 14
        self.y_off = 160
        self.width_all = 70

        self.indices     = ((0, 1, 2), (0, 2, 3))

    def set_color_buttons(self, context):
        cb  = context.scene.color_buttons
        cba = context.scene.color_buttons_active

        self.color        = (cb[0], cb[1], cb[2], cb[3])
        self.color_active = (cba[0], cba[1], cba[2], cba[3])

    def create_batches(self, context):

        if context.scene.h_dock == "0":
            self.x_off = 14
        elif context.scene.h_dock == "1":
            self.x_off = context.region.width - 100
        else:
            self.x_off = ((context.region.width - self.width_all) / 2.0) - 1

        # bottom left, top left, top right, bottom right
        # (左下(x,y),左上(x,y),右上(x,y),右下(x,y))

        l_move = self.x_off - 50
        r_move = self.x_off + 60
        m_move = self.x_off + 20
        mouse_he = 120

        self.vertices_left   = ((l_move, 30 + self.y_off), (l_move, mouse_he + self.y_off), (l_move + 60, mouse_he + self.y_off), (l_move + 60, 30 + self.y_off))
        self.vertices_right  = ((r_move, 30 + self.y_off), (r_move, mouse_he + self.y_off), (r_move + 60, mouse_he + self.y_off), (r_move + 60, 30 + self.y_off))

        self.vertices_middle = ((m_move, 60 + self.y_off), (m_move, mouse_he + self.y_off), (m_move + 30, mouse_he + self.y_off), (m_move + 30, 60 + self.y_off))


        self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

        self.batch_left_button   = batch_for_shader(self.shader, 'TRIS', {"pos" : self.vertices_left},   indices = self.indices)
        self.batch_right_button  = batch_for_shader(self.shader, 'TRIS', {"pos" : self.vertices_right},  indices = self.indices)
        self.batch_middle_button = batch_for_shader(self.shader, 'TRIS', {"pos" : self.vertices_middle}, indices = self.indices)

    def __get_color(self, key_state):
        if key_state is True:
            return self.color_active
        else:
            return self.color

    def __set_color(self, key_state):
        self.shader.uniform_float("color", self.__get_color(key_state))

    def draw_buttons(self, left, middle, right):

        self.shader.bind()

        self.__set_color(left)

        self.batch_left_button.draw(self.shader)

        self.__set_color(middle)
        self.batch_middle_button.draw(self.shader)

        self.__set_color(right)
        self.batch_right_button.draw(self.shader)

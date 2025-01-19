from colorama import Fore, Back, Style, init

# تهيئة colorama
init(autoreset=True)

class BoardRenderer:
    def __init__(self, board):
        self.board = board
        self.colors = [Fore.RED, Fore.BLUE]  # ألوان اللاعبين (أحمر للاعب 1، أزرق للاعب 2)

    def render(self):
        # إنشاء شبكة الرقعة
        grid = [[' ' for _ in range(15)] for _ in range(15)]

        # رسم القواعد (الخانات الأساسية) لكل لاعب
        for player_id in range(2):
            color = self.colors[player_id]
            for i in range(4):
                x, y = self.get_home_position(player_id, i)
                grid[x][y] = color + '■' + Style.RESET_ALL  # ■ تمثل القطعة في القاعدة

        # رسم المسارات الخاصة بكل لاعب
        for player_id in range(2):
            color = self.colors[player_id]
            for pos in range(57):
                x, y = self.get_path_position(pos, player_id)
                if grid[x][y] == ' ':
                    if pos == 0:  # بداية الطريق
                        grid[x][y] = color + 'S' + Style.RESET_ALL  # S تمثل البداية
                    elif pos == 56:  # نهاية الطريق (النجمة)
                        grid[x][y] = color + '★' + Style.RESET_ALL  # ★ تمثل النهاية
                    elif 51 <= pos <= 55:  # الخانات الأخيرة للاعب
                        grid[x][y] = color + '.' + Style.RESET_ALL  # . تمثل الخانات الأخيرة
                    else:
                        grid[x][y] = Fore.WHITE + '.' + Style.RESET_ALL  # . تمثل المسار

        # رسم القطع على الرقعة
        for player_id, player in enumerate(self.board.players):
            color = self.colors[player_id]
            for piece in player.pieces:
                if piece.position != -1:
                    x, y = self.get_path_position(piece.position, player_id)
                    if piece.position == 56:  # إذا وصلت إلى الهدف
                        grid[x][y] = color + '★' + Style.RESET_ALL  # ★ تمثل القطعة في الهدف
                    else:  # إذا كانت القطعة في الطريق
                        grid[x][y] = color + '●' + Style.RESET_ALL  # ● تمثل القطعة في الطريق

        # طباعة الرقعة
        for row in grid:
            print(' '.join(row))

    def get_home_position(self, player_id, piece_id):
        """
        إرجاع إحداثيات الخانة الأساسية للقطعة.
        """
        if player_id == 0:
            return (piece_id, 0)
        elif player_id == 1:
            return (0, 14 - piece_id)
        return (0, 0)

    def get_path_position(self, position, player_id):
        """
        إرجاع إحداثيات المسار بناءً على الموضع ولاعب.
        """
        if player_id == 0:
            return (position // 10, position % 10)
        elif player_id == 1:
            return (position % 10, 14 - (position // 10))
        return (0, 0)
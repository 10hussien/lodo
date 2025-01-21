from colorama import Fore, Back, Style, init

# تهيئة colorama
init(autoreset=True)

class Board:
    def __init__(self):
        self.safe_spots = {0, 8, 13, 21, 26, 34, 39, 47}  # الخانات الآمنة
        self.path_length = 56  # طول المسار من البداية إلى النهاية

    def is_safe_spot(self, position):
        """تحقق إذا كانت الخانة آمنة."""
        return position in self.safe_spots

    def is_wall(self, players, position):
        """تحقق إذا كان هناك جدار في الخانة (قطعتان أو أكثر من نفس اللاعب)."""
        for player in players:
            count = player.pieces.count(position)
            if count >= 2:
                return True
        return False

    def get_pieces_at_position(self, players, position):
        """احصل على القطع في موقع معين مع ألوانها."""
        pieces = []
        for player in players:
            for i, pos in enumerate(player.pieces):
                if pos == position:
                    pieces.append((i, player.color))
        return pieces

    def get_board_state(self, players):
        """احصل على حالة اللوحة الحالية (مواقع جميع قطع اللاعبين)."""
        board_state = {}
        for player in players:
            board_state[player.name] = player.pieces.copy()
        return board_state

    def print_base_pieces(self, players):
        """طباعة القطع في القاعدة كمربعات ملونة."""
        print("\nPieces in the Base:")
        for player in players:
            pieces_in_base = player.pieces.count(-1)
            if pieces_in_base > 0:
                # مربعات ملونة لكل لاعب
                if player.color == "Red":
                    squares = Fore.RED + " ■ " * pieces_in_base
                elif player.color == "Blue":
                    squares = Fore.BLUE + " ■ " * pieces_in_base
                print(f"{player.name} ({player.color}): {squares}")
            else:
                # دوائر إذا لم تتبقى قطع في القاعدة
                if player.color == "Red":
                    circles = Fore.RED + " ● "
                elif player.color == "Blue":
                    circles = Fore.BLUE + " ● "
                print(f"{player.name} ({player.color}): {circles}")

    def print_board(self, players):
        """طباعة لوحة اللعبة بتنسيق أفقي مع فصل مصفوفة كل لاعب."""
        self.print_base_pieces(players)  # طباعة القطع في القاعدة
        print("\nGame Board:")
        print("=" * 80)

        # طباعة مصفوفة كل لاعب على حدة
        for player in players:
            print(f"\n{player.name}'s Board ({player.color}):")
            print("-" * 80)
            for i in range(0, self.path_length + 1, 10):  # طباعة 10 خلايا في كل صف
                for j in range(i, min(i + 10, self.path_length + 1)):
                    # احصل على القطع في هذا الموقع
                    pieces = self.get_pieces_at_position(players, j)
                    # تحديد لون الخلية والمحتوى
                    if j in self.safe_spots:
                        cell_color = Back.YELLOW + Fore.BLACK  # الخانات الآمنة
                    elif len(pieces) >= 2 and all(p[1] == pieces[0][1] for p in pieces):
                        # قطعتان أو أكثر من نفس اللاعب
                        cell_color = Back.BLUE + Fore.WHITE if pieces[0][1] == "Blue" else Back.RED + Fore.WHITE
                    elif len(pieces) >= 1:
                        # قطع مختلطة أو قطعة واحدة
                        cell_color = Back.WHITE + Fore.BLACK
                    else:
                        # خلية فارغة
                        cell_color = Back.WHITE + Fore.BLACK
                    # إعداد محتوى الخلية
                    cell_content = f" {j:2} "
                    if pieces:
                        if j in self.safe_spots:
                            # خانة آمنة: الحفاظ على لون الخلفية، تغيير لون النص
                            cell_content = f" {j:2} "
                            for p in pieces:
                                if p[1] == player.color:  # عرض قطع اللاعب الحالي فقط
                                    cell_content += Fore.RED + "■" if p[1] == "Red" else Fore.BLUE + "■"
                        else:
                            # خانة عادية: تغيير لون الخلفية، الحفاظ على لون النص
                            cell_content = f" {j:2} "
                            for p in pieces:
                                if p[1] == player.color:  # عرض قطع اللاعب الحالي فقط
                                    cell_content += Fore.RED + "■" if p[1] == "Red" else Fore.BLUE + "■"
                    # طباعة الخلية
                    print(cell_color + cell_content, end="")
                print("\n" + "-" * 80)
        print("=" * 80)
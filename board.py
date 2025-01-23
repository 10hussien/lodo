from colorama import Fore, Back, Style, init
from lodo_rulse import Rules  
# تهيئة colorama
init(autoreset=True)

class Board:
    def __init__(self):
        self.rules = Rules()   # طول المسار من البداية إلى النهاية

    def is_safe_spot(self, position):
        """تحقق إذا كانت الخانة آمنة."""
        return self.rules.is_safe_spot(position)

    def is_wall(self, players, position):
        """تحقق إذا كان هناك جدار في الخانة (قطعتان أو أكثر من نفس اللاعب)."""
        return self.rules.is_wall(players, position)

    def should_return_piece(self, players, position):
        """تحقق إذا كان يجب إعادة القطعة إلى القاعدة."""
        return self.rules.should_return_piece(players, position)

    def get_pieces_at_position(self, players, position):
        """احصل على القطع في موقع معين مع ألوانها."""
        return self.rules.get_pieces_at_position(players, position)
    
    def get_board_state(self, players):
        """احصل على حالة اللوحة الحالية (مواقع جميع قطع اللاعبين)."""
        return self.rules.get_board_state(players)

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
            for i in range(0, self.rules.path_length + 1, 10):  # استخدام path_length من rules
                for j in range(i, min(i + 10, self.rules.path_length + 1)):
                    # احصل على القطع في هذا الموقع
                    pieces = self.get_pieces_at_position(players, j)
                    # تحديد لون الخلية والمحتوى
                    if j in self.rules.safe_spots:  # استخدام safe_spots من rules
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
                        if j in self.rules.safe_spots:  # استخدام safe_spots من rules
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
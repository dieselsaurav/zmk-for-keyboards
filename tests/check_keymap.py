"""Regression checks for the Corne OS layer banks; run with python3 tests/check_keymap.py."""
from pathlib import Path
import re
import unittest

SOURCE = (Path(__file__).resolve().parents[1] / "config/corne.keymap").read_text()
CLEAN = re.sub(r"//[^\n]*|/\*[\s\S]*?\*/", "", SOURCE)
DEFINES = {key: int(value) for key, value in re.findall(r"#define\s+(\w+)\s+(\d+)", CLEAN)}
LAYERS = re.findall(
    r'(\w+_layer)\s*\{\s*display-name\s*=\s*"([^"]+)";\s*bindings\s*=\s*<([\s\S]*?)>;',
    CLEAN,
)
def bindings(body):
    return [" ".join(part.split()) for part in re.findall(r"&\w+[^&]*", body)]

BANKS = [bindings(body) for _, _, body in LAYERS]
NAMES = ["BASE", "NAV", "NUM", "MEDIA", "SYM", "FUN", "MOUSE"]

class KeymapChecks(unittest.TestCase):
    def test_layer_sizes_and_order(self):
        self.assertEqual(len(LAYERS), 14)
        self.assertEqual([name for _, name, _ in LAYERS],
                         [f"{os} {name}" for os in ["MAC", "WIN"] for name in NAMES])
        for i, row in enumerate(BANKS):
            self.assertEqual(len(row), 42, f"layer {i}")
        for i, name in enumerate(NAMES):
            self.assertEqual(DEFINES[name], i)
            self.assertEqual(DEFINES["WIN_" + name], i + 7)

    def test_only_intended_bank_differences(self):
        swaps = {"LGUI": "LCTRL", "LCTRL": "LGUI", "RGUI": "RCTRL", "RCTRL": "RGUI"}
        for i in range(7):
            for position, mac in enumerate(BANKS[i]):
                expected = re.sub(r"\b(LGUI|LCTRL|RGUI|RCTRL)\b",
                                  lambda m: swaps[m[0]], mac)
                expected = expected.replace("&mt LGUI ESC", "&mt LCTRL ESC")
                expected = re.sub(r"\bLG\(", "LC(", expected)
                expected = re.sub(r"&lt (MEDIA|NAV|MOUSE|SYM|NUM|FUN)\b",
                                  r"&lt WIN_\1", expected)
                self.assertEqual(BANKS[i + 7][position], expected,
                                 f"layer {i}, position {position}")

    def test_selectors_and_terminal_control(self):
        for index in [3, 10]:
            self.assertEqual(BANKS[index][1:3], ["&to BASE", "&to WIN_BASE"])
        for index in [0, 7]:
            self.assertEqual(BANKS[index][12], "&mt LCTRL ESC")
            self.assertEqual(BANKS[index][23], "&hyper")
        self.assertEqual(BANKS[0][13], "&mt LGUI A")
        self.assertEqual(BANKS[7][13], "&mt LCTRL A")
        self.assertEqual(BANKS[0][15], "&mt LCTRL D")
        for base, prefix in [(0, ""), (7, "WIN_")]:
            for pos, layer, tap in [(36,"MEDIA","ESC"), (37,"NAV","SPACE"),
                                    (38,"MOUSE","TAB"), (39,"SYM","RET"),
                                    (40,"NUM","BSPC"), (41,"FUN","DEL")]:
                self.assertEqual(BANKS[base][pos], f"&lt {prefix}{layer} {tap}")

    def test_clipboard(self):
        for nav, modifier in [(1, "LG"), (8, "LC")]:
            self.assertEqual(BANKS[nav][6:11],
                [f"&kp {modifier}({key})" for key in ["LS(Z)", "V", "C", "X", "Z"]])
        for win, prefix in [(False, ""), (True, "win_")]:
            for action, key, positions in [("copy","C","26 27"), ("paste","V","27 28"),
                                           ("cut","X","26 28")]:
                body = re.search(r"combo_" + prefix + action + r"\s*\{([^}]+)\}", CLEAN)[1]
                self.assertIn(f"bindings = <&kp {'LC' if win else 'LG'}({key})>;", body)
                self.assertIn(f"key-positions = <{positions}>;", body)
                scope = re.search(r"layers = <([^>]+)>", body)[1].split()
                self.assertEqual(scope, [("WIN_" if win else "") + n for n in NAMES])

    def test_original_global_combos_and_hyper(self):
        combos = re.findall(r"combo_(\w+)\s*\{([^}]+)\}", CLEAN)
        self.assertEqual(len(combos), 17)
        self.assertEqual(sum("layers =" not in body for _, body in combos), 11)
        for line in ["<&macro_press &kp LGUI &kp LALT &kp LCTRL &kp LSHFT>",
                     "<&macro_pause_for_release>",
                     "<&macro_release &kp LGUI &kp LALT &kp LCTRL &kp LSHFT>"]:
            self.assertIn(line, CLEAN)

if __name__ == "__main__":
    unittest.main()

# Mac and Windows setup

## Select the operating system

Hold the **leftmost ESC thumb key** for the Media layer, then tap:
- **Q**: Mac mode.
- **W**: Windows mode.

Release both keys before typing. The left display and ZMK Studio show
`MAC BASE` or `WIN BASE`; held layers have matching prefixes.
Mac mode is the startup default. Select Windows again after reboot.
Sleep does not intentionally change the mode. OS mode is global, not remembered per Bluetooth profile.

Bluetooth profile selection and USB/Bluetooth output selection retain their existing bindings.
Switching a Bluetooth profile does not select Mac/Windows mode.

## Modifier positions

| Physical key held | Mac | Windows |
| --- | --- | --- |
| A | Command | Ctrl |
| S | Option | Alt |
| D | Ctrl | Windows |
| F | Shift | Shift |
| J | Shift | Shift |
| K | Ctrl | Windows |
| L | Right Option | Right Alt (AltGr on some layouts) |
| Quote | Right Command | Right Ctrl |
| Outer left Escape | **Ctrl** | **Ctrl** |

Tap these keys for their original letters or Escape. Outer Escape/Ctrl is at
the left edge of the home row, separate from the ESC/Media thumb.
For example, hold A and press C to copy on either OS. For terminal Ctrl+C
on Mac, hold outer Escape or D and press C.
The Hyper key still holds Ctrl+Alt+Shift+GUI on both systems.

All modifier keys on the utility layers follow the same Ctrl/GUI swap.
QWERTY, symbols, mouse, media, RGB and all existing combo key positions are preserved.
This does not translate every app shortcut: use Command+Tab on Mac and Alt+Tab
on Windows, and use the shortcut expected by your terminal application.
Use the same host input layout (for example US English) on both computers for matching symbols.

## Thumb layers

| Thumb, from left to right | Tap | Hold: Mac / Windows layer |
| --- | --- | --- |
| Left outer | Escape | Media: 3 / 10 |
| Left middle | Space | Navigation: 1 / 8 |
| Left inner | Tab | Mouse: 6 / 13 |
| Right inner | Enter | Symbols: 4 / 11 |
| Right middle | Backspace | Numbers: 2 / 9 |
| Right outer | Delete | Function keys: 5 / 12 |

Mac base is layer 0; Windows base is layer 7. Each bank uses native ZMK
bindings, so ZMK Studio can edit either bank without custom behavior code.
If changing shortcuts in Studio, edit the corresponding layer in both banks.

## Clipboard

| Action | Combo or NAV position | Mac output | Windows output |
| --- | --- | --- | --- |
| Copy | X+C combo; NAV at I | Command+C | Ctrl+C |
| Paste | C+V combo; NAV at U | Command+V | Ctrl+V |
| Cut | X+V combo; NAV at O | Command+X | Ctrl+X |
| Undo | NAV at P | Command+Z | Ctrl+Z |
| Redo | NAV at Y | Command+Shift+Z | Ctrl+Shift+Z |

Redo uses Ctrl+Shift+Z on Windows; some applications require Ctrl+Y.
Existing combo timing and prior-idle settings remain unchanged.
Clipboard combos are scoped to the highest active layer's OS bank.
Other original combos remain global.

## Build and install

1. In your fork, open **Actions**. If GitHub says workflows are disabled for
   this fork, click **I understand my workflows, go ahead and enable them**.
2. A push changing `config/` starts **Build ZMK firmware**. If needed,
   select that workflow, choose **Run workflow**, select this PR's branch,
   and run it. Wait for the complete build matrix to succeed.
3. Download the **firmware** artifact from the successful run. Keep a copy
   of your previous working firmware and any Studio changes before installing.
4. Choose files matching your actual controller and display:
   - OLED: the `corne_left` and `corne_right` builds without `nice_view`.
   - Nice!View: the left and right builds including
     `nice_view_adapter nice_view`.
   The matrix targets `nice_nano//zmk`; this repository's README identifies
   nice!nano v2. Confirm your hardware matches before choosing binaries.
5. Connect the left half by USB data cable. Double-tap its reset button to
   enter the UF2 bootloader. Copy the matching **left** `.uf2` to the
   bootloader drive; it reboots automatically.
6. Repeat for the right half using the matching **right** `.uf2`.
   Flash both from the same successful build because upstream ZMK tracks main.
   A normal update does not require the `settings_reset` firmware.
7. If you previously saved changes through ZMK Studio, connect the left half
   in Studio and use **Restore Stock Settings** to load the new compiled
   layout, then save as prompted. This discards previous Studio remaps,
   so record them first. Flashing alone can leave saved remaps in use.
8. Verify Mac/Windows selection, A+C, the three clipboard combos, NAV undo/redo,
   terminal Ctrl+C, all six thumb layers, and profile switching on the devices.

## Recovery

If the layout is unusable, use each half's physical reset button to enter
the bootloader and copy its previous matching firmware back. Restore the
old compiled keymap through Studio if saved Studio settings override it.
Use settings-reset only for a diagnosed pairing/settings problem, following
ZMK's reset instructions; it is not the routine way to install this layout.

## Validation boundaries

The regression check in `tests/check_keymap.py` checks layer size and order,
mode selectors, Windows layer targets, OS-specific shortcuts and combos,
and preservation of terminal Ctrl and the Hyper macro.
It is not a firmware compiler or a hardware test.
GitHub Actions performs the actual firmware builds; installation and real
host behavior must still be checked on your keyboard.

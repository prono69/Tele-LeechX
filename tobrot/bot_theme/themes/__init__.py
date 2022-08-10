from tobrot import BOT_THEME
from tobrot.bot_theme.themes import fx_optimised, fx_minimal

def BotTheme():
    if BOT_THEME == "fx-optimised-theme":
        return fx_optimised.TXStyle()
    elif BOT_THEME == "fx-minimal-theme":
        return fx_minimal.TXStyle()
    else:
        return fx_optimised.TXStyle()

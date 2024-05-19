import TokenGrabber
import CreatorDiscordUser
import config


def generate(number):
    email = config.email.replace("CODE", f"+{number}")
    result = CreatorDiscordUser.register_discord_account(email, config.username, config.global_name,
                                                         config.password, config.day,
                                                         config.month, config.year, config.invites_link, config.proxy)
    if result == False:
        generate(number)
        return
    TokenGrabber.Grabber().GetDiscordToken(email, config.password)

if __name__ == "__main__":
    for number in range(4, 500):
        generate(number)
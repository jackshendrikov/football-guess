shorten_teams = dict([('Brighton & Hove Albion', 'Brighton'), ('Tottenham Hotspur', 'Tottenham'),
                      ('Wolverhampton Wanderers', 'Wolverhampton'), ('West Bromwich Albion', 'West Bromwich'),
                      ('SSC Napoli', 'Napoli'), ('Parma Calcio 1913', 'Parma'), ('Deportivo Alaves', 'Deportivo'),
                      ('Paris Saint-Germain', 'PSG'), ('RasenBallsport Leipzig', 'RB Leipzig'),
                      ('Eintracht Frankfurt', 'Eintracht'), ('Borussia Dortmund', 'Borussia D'),
                      ('Bayer Leverkusen', 'Bayer'), ('Borussia Moenchengladbach', 'Borussia M'),
                      ('1. FC Köln', 'FC Köln'), ('Arminia Bielefeld', 'Arminia'), ('Werder Bremen', 'Werder'),
                      ('Hertha Berlin', 'Hertha'), ('FC Kolos Kovalivka', 'FC Kolos'),
                      ('Inhulets Petrove', 'Inhulets'), ('Rukh Vynnyky', 'Rukh')])


def shorten_name(team):
    return shorten_teams[team] if team in shorten_teams.keys() else \
        team.replace('United', 'Utd').replace('Manchester', 'Man.')

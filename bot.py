import discord
from discord.ext import tasks
import re
import requests
import json
import datetime
from dateutil import tz
from requests_html import AsyncHTMLSession
import statsapi
import random
from collections import defaultdict
import asyncio

testmode = False

manager = "Manager"
pictureadder = "picture adder"
teams = { "arizona diamondbacks" :"ari",
        "washington nationals":"was",
        "miami marlins":"mia",
        "pittsburgh pirates":"pit",
        "milwaukee brewers":"mil",
        "toronto blue jays":"tor",
        "baltimore orioles":"bal",
        "texas rangers":"tex",
        "colorado rockies":"col",
        "detroit tigers":"det",
        "oakland athletics":"oak",
        "houston astros":"hou",
        "seattle mariners":"sea",
        "atlanta braves":"atl",
        "philadelphia phillies":"phi",
        "boston red sox":"bos",
        "cleveland guardians":"cle",
        "cincinnati reds":"cin",
        "minnesota twins":"min",

        "tampa bay rays":"tb",
        "san francisco giants":"sf",
        "kansas city royals":"kc",
        "san diego padres":"sd",
        "st. louis cardinals":"stl",

        "new york yankees":"nyy",
        "new york mets":"nym",
        "los angeles dodgers":"lad",
        "los angeles angels":"laa",
        "chicago cubs":"chc",
        "chicago white sox":"chw"
        }

lookup = { "arizona diamondbacks" :"ari",
        "washington nationals":"was",
        "miami marlins":"mia",
        "pittsburgh pirates":"pit",
        "milwaukee brewers":"mil",
        "toronto blue jays":"tor",
        "baltimore orioles":"bal",
        "texas rangers":"tex",
        "colorado rockies":"col",
        "detroit tigers":"det",
        "oakland athletics":"oak",
        "houston astros":"hou",
        "seattle mariners":"sea",
        "atlanta braves":"atl",
        "philadelphia phillies":"phi",
        "boston red sox":"bos",
        "cleveland guardians":"cle",
        "cincinnati reds":"cin",
        "minnesota twins":"min",

        "tampa bay rays":"tb",
        "san francisco giants":"sf",
        "kansas city royals":"kc",
        "san diego padres":"sd",
        "st. louis cardinals":"stl",

        "new york yankees":"nyy",
        "new york mets":"nym",
        "los angeles dodgers":"lad",
        "los angeles angels":"ana",
        "chicago cubs":"chc",
        "chicago white sox":"cws"
        }
logo2team = { "diamondbacks" :"arizona diamondbacks",
        "nationals":"washington nationals",
        "marlins":"miami marlins",
        "pirates":"pittsburgh pirates",
        "brewers":"milwaukee brewers",
        "blue jays":"toronto blue jays",
        "orioles":"baltimore orioles",
        "rangers":"texas rangers",
        "rockies":"colorado rockies",
        "tigers":"detroit tigers",
        "athletics":"oakland athletics",
        "astros":"houston astros",
        "mariners":"seattle mariners",
        "braves":"atlanta braves",
        "phillies":"philadelphia phillies",
        "red sox":"boston red sox",
        "guardians":"cleveland guardians",
        "reds":"cincinnati reds",
        "twins":"minnesota twins",

        "rays":"tampa bay rays",
        "giants":"san francisco giants",
        "royals":"kansas city royals",
        "padres":"san diego padres",
        "cardinals":"st. louis cardinals",

        "yankees":"new york yankees",
        "mets":"new york mets",
        "dodgers":"los angeles dodgers",
        "angels":"los angeles angels",
        "cubs":"chicago cubs",
        "white sox":"chicago white sox",
        }
team2id = {'arizona diamondbacks': 109, 'washington nationals': 120, 'miami marlins': 146, 'pittsburgh pirates': 134, 'milwaukee brewers': 158, 'toronto blue jays': 141, 'baltimore orioles': 110, 'texas rangers': 140, 'colorado rockies': 115, 'detroit tigers': 116, 'oakland athletics': 133, 'houston astros': 117, 'seattle mariners': 136, 'atlanta braves': 144, 'philadelphia phillies': 143, 'boston red sox': 111, 'cleveland guardians': 114, 'cincinnati reds': 113, 'minnesota twins': 142, 'tampa bay rays': 139, 'san francisco giants': 137, 'kansas city royals': 118, 'san diego padres': 135, 'st. louis cardinals': 138, 'new york yankees': 147, 'new york mets': 121, 'los angeles dodgers': 119, 'los angeles angels': 108, 'chicago cubs': 112, 'chicago white sox': 145}
id2team = {109: 'arizona diamondbacks', 120: 'washington nationals', 146: 'miami marlins', 134: 'pittsburgh pirates', 158: 'milwaukee brewers', 141: 'toronto blue jays', 110: 'baltimore orioles', 140: 'texas rangers', 115: 'colorado rockies', 116: 'detroit tigers', 133: 'oakland athletics', 117: 'houston astros', 136: 'seattle mariners', 144: 'atlanta braves', 143: 'philadelphia phillies', 111: 'boston red sox', 114: 'cleveland guardians', 113: 'cincinnati reds', 142: 'minnesota twins', 139: 'tampa bay rays', 137: 'san francisco giants', 118: 'kansas city royals', 135: 'san diego padres', 138: 'st. louis cardinals', 147: 'new york yankees', 121: 'new york mets', 119: 'los angeles dodgers', 108: 'los angeles angels', 112: 'chicago cubs', 145: 'chicago white sox'}




class callbackwrapper:
    def __init__(self):
        self.channel = None
        self.test = None
        self.replies = {}
        self.extracmds = {}
        self.client = discord.Client()
        self.client = discord.Client()
        self.points = defaultdict(int)
    def start(self):
        print("starting")
        key = None
        with open("key", "r") as kf:
            key = kf.readline().strip()
            print("key obtained")
        self.client.run(key)
    async def announce(self, message):
        if testmode == True:
            await self.test.send(message)
        else:
            await self.channel.send(message)
    async def on_ready(self):
        self.channel = self.client.get_channel(829922100381745190)
        self.test = self.client.get_channel(829942104146837504)
        self.update_replies()
        self.load_points()
        self.on_start_test()
        announce_scheduled.start()

    def on_start_test(self):
        print("Bot started")
    def load_points(self):
        with open("points.txt", "r") as pf:
            for line in pf:
                u,p = line.strip().rsplit("\t", 1)
                p = int(p)
                self.points[u] = p
        print(self.points)

    def update_replies(self):
        self.replies = {}
        self.extracmds = {}
        with open("replies.txt", "r") as rf:
            for line in rf:
                if line.strip() == "" or line[0] == "C":
                    continue
                i, o = line.split("I:O")
                i = i.strip()
                o = o.strip()
                if i[0] == "!":
                    a = i[1:].split()
                    for i in range(1, len(a)):
                        a[i] = int(a[i])
                    self.extracmds[a[0]] = {"arg": a[1:], "msg": o}
                else:
                    self.replies[i] = o


    async def cmd_tf(self, user, channel, msg, ogcmd, *args):
        await self.send(channel, ":monkas:")
        
    def to_bilas(self, away, home):
        away = away.lower()
        home = home.lower()
        if away[:3] == "st.":
            away = "st louis cardinals"
        if home[:3] == "st.":
            home = "st louis cardinals"

        away = "-".join(away.split())
        home = "-".join(home.split())
        return f"<http://bilasport.net/game/{home}-vs-{away}-1.html>"

    def getlogo(self, teamname):
        return teams[teamname.lower()]

    async def cmd_fees(self, user, channel, msg, ogcmd, *args):
        if len(args) != 2:
            print(msg, args)
            await self.send(channel, f"@{user}, usage is !fees <$initial investment> <ROI%>")
            return
        await self.cmd_profit(user, channel, msg, ogcmd, *args)
    async def cmd_profit(self, user, channel, msg, ogcmd, *args):
        if len(args) != 2:
            print(msg, args)
            await self.send(channel, f"@{user}, usage is !profit <$initial investment> <ROI%>")
            return

        ROI = None
        try:
            a = args[1]
            if a[-1] == '%':
                a = a[:-1]
            ROI = float(a)
        except ValueError:
            await self.send(channel, f"@{user}, ROI has to be a percentage")
            return
        inv = None
        try:
            a = args[0]
            if a[0] == "$":
                a = a[1:]
            elif a[-1] == "$":
                a = a[:-1]
            inv = float(a)
            if inv <= 0:
                raise ValueError
        except ValueError:
            await self.send(channel, f"@{user}, your initial investment has to be positive")
            return

        ROI /= 100
        tiers = [0, 0.25, 1.00, float("inf")]
        fees = [0.15, 0.30, 0.45]
        feepercent = 0
        if ROI < 0:
            feepercent = 0
        else:
            for i in range(len(tiers)-1):
                if ROI > tiers[i+1]:
                    feepercent += fees[i] * (tiers[i+1] - tiers[i])
                if tiers[i+1] >= ROI:
                    feepercent += fees[i] * (ROI - tiers[i])
                    break


        profitpercent = ROI - feepercent
        dp = abs(profitpercent)
        pl = lambda x: x[0] if profitpercent >= 0 else x[1]

        #msg = f"For an ROI of {ROI*100:.2f}%, you would pay {feepercent*100:.2f}% of the initial investment in fees. "
        #msg += f"You would {pl(['profit', 'lose'])} {dp*100:.2f}% of the initial investment.\n"
        msg = f"For an initial investment of ${inv:.2f} and {ROI*100:.2f}% ROI:```"
        msg += f"Portfolio value:            ${inv*(ROI+1):.2f}\n"
        msg += f"Return:                    {pl([' ','-'])}${abs(ROI*inv):.2f}\n"
        msg += f"Fees:                       ${inv*feepercent:.2f}\n"
        msg += f"Portfolio value after fees: ${inv*(profitpercent+1):.2f}\n"
        msg += f"Profit:                    {pl([' ','-'])}${inv*(dp):.2f}\n"
        msg += f"Percent profit:             {profitpercent*100:.2f}%```"
        if round(inv*(profitpercent),2) >= inv:
            msg += f"RHF to the moon! :peeporocket: :moon:"
        elif profitpercent <= 0:
            msg += f"RHF pls :ohno: :prayge:"

        await self.send(channel, msg)






    async def cmd_games(self, user, channel, msg, ogcmd, *args):
        resp = requests.get("https://www.espn.com/mlb/schedule").text
        i = resp.index("sched-container")
        i = resp.index("<tbody>",i) + 8
        i = resp.index(">",i) + 1
        end = resp.index("table-caption", i)
        stuff = []
        while True:
            away = resp.index("abbr title",i) + 12
            if away > end:
                break
            away2 = resp.index('"',away)
            home = resp.index("abbr title",away2) + 12
            home2 = resp.index('"',home)
            status = resp.index('<td', home2) + 4
            status2 = 0
            time = ""

            if (resp[status:status+4] == "data"):

                status = resp.index("T", status) + 1
                status2 = resp.index("Z", status)
                
                a,b = self.T_to_pdt(resp[status:status2])
                time = self.prettytime(a,b)
            else:
                status = resp.index(">", status) + 1
                statusm = resp.index(">", status) + 1
                status2 = resp.index("<", statusm)
                time = resp[statusm:status2]
                if time == "LIVE":
                    time = "Live"
                else:
                    status2 = resp.index("<", status)
                    time = resp[status:status2]
                    if time == "Postponed": time = "Pstpn"
                    else: time = "Ended"

            stuff.append((resp[away:away2],resp[home:home2],time))
            
            i = status
        i = len(stuff)//2
        stuff1 = stuff[:i]
        stuff2 = stuff[i:]

        print("yo")
        msg1 = "\n".join(f"{z}:\t:{self.getlogo(x)}: {x}  @  :{self.getlogo(y)}: {y}   |   {self.to_bilas(x,y)}"
                for x,y,z in stuff1)
        msg2 = "\n".join(f"{z}:\t:{self.getlogo(x)}: {x}  @  :{self.getlogo(y)}: {y}   |   {self.to_bilas(x,y)}"
                for x,y,z in stuff2)
            
        await self.send(channel, msg1)
        await self.send(channel, msg2)


    async def cmd_om(self, user, channel, msg, ogcmd, *args):
        i = 3
        while msg.content[i] != ' ':
            i += 1

        spaced = " ".join(list(msg.content[i:]))
        ol = spaced.split("o")
        ou = []
        for s in ol:
            ou.extend(s.split("O"))
        await self.send(channel, ":omegalul:".join(ou))
    async def cmd_game(self, user, channel, msg, ogcmd, *args):
        if args[0].lower() == "info":
            await self.cmd_gameinfo(user, channel, msg, ogcmd, *args[1:])
    async def cmd_tilas(self, user, channel, msg, ogcmd, *args):
        await self.cmd_bilas(user, channel, msg, ogcmd, *args)
    def getgame(self, team):
        resp = requests.get("https://bilasport.com/mlb.html").text
        print(resp)
        
        idxs = [m.start() for m in re.finditer("scoreboard scoreboard", resp)]
        
        cur = None
        for start in idxs:
            end = start + 1350
            cur = resp[start:end]
            if cur.find(team) >= 0:
                break

        teams = [m.start() for m in re.finditer("team-name", cur)]
        
        home = cur[ cur.index('>', teams[0])+1 : cur.index('<', teams[0]) ].lower()
        away = cur[ cur.index('>', teams[1])+1 : cur.index('<', teams[1]) ].lower()
        
        return home, away

    async def cmd_bilas(self, user, channel, msg, ogcmd, *args):
        if len(args) == 0:
            await self.send(channel, f"@{user}, usage is !{ogcmd} <team name>")
            return
        team = " ".join(args)
        home, away = self.getgame(team)
        
        msg = f"{self.to_bilas(away, home)}"
        await self.send(channel, msg)

    def prettytime(self, h,m):
        x = "AM"
        if h > 12:
            h -= 12
            x = "PM"

        if m < 10: m =f"0{m}"
        return f"{h}:{m} {x}"
    def T_to_pdt(self, time):

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        c = time.split(":")
        a = None
        b = None
        if len(c) == 3:
            a,b,_ = c
        elif len(c) == 2:
            a,b = c
        else:
            raise Exception
        todate = datetime.date.today()
        d = datetime.datetime.strptime(f"{str(todate)} {a}:{b}", "%Y-%m-%d %H:%M")#hour = a_, minute=b_)

        utc = d.replace(tzinfo=from_zone)
        local = d.astimezone()
        a = utc + local.utcoffset()
        h = a.hour
        m = a.minute
        return h,m


    def gameinfo(self, team):
        todate = datetime.date.today()
        y,m,d = str(todate).split("-")
        todate = "/".join([m,d,y])
        sched = statsapi.schedule(start_date = todate,end_date = todate, team = team)
        state = None
        for g in sched:
            away = g["away_name"]
            home = g["home_name"]
            status = g["status"]
            if status == "Final" or status == "Game Over":
                state = "Final"
            elif status == "In Progress":
                state = g['inning_state'][:3] + " " + g['surrent_inning']
            else:
                start = g["game_datetime"].split("T")[1]
                a,b = self.T_to_pdt(start)
                gamestart = datetime.time(hour=a, minute=b)
                curtime = datetime.datetime.now().time()
                if gamestart >= curtime:
                    state = f"Start time: {self.prettytime(a,b)}"
                else:
                    state = f"Delayed"
        return (away, home, state)

    async def cmd_gameinfo(self, user, channel, msg, ogcmd, *args):
        if len(args) == 0:
            await self.send(channel, f"@{user}, usage is !gameinfo [team name]")
            return
        
        team = " ".join(args)
        try:
            team = logo2team[team]
            team = team2id[team]
        except KeyError:
            await self.send(channel, f'Could not find team "{" ".join(args)}"')
            return
        
        todate = datetime.date.today()
        y,m,d = str(todate).split("-")
        todate = "/".join([m,d,y])

        sched = statsapi.schedule(start_date = todate,end_date = todate, team = team)
        
        st = "" if len(sched) == 1 else "Double header\n"
        ended = True
        for g in sched:
            away = g["away_name"]
            home = g["home_name"]
            status = g["status"]
            print(status)
            if status == "Final" or status == "Game Over":
                st += f"{away} at {home}\n{g['away_score']} - {g['home_score']}\nFinal\n"
            elif status == "Scheduled":
                st += f"{away} at {home} {status}\n"
                ended = False
            elif status == "In Progress":
                st += f"{away} at {home}\n"
                st += f"{g['away_score']} - {g['home_score']}\n{g['inning_state'][:3]} {g['current_inning']}\n" 
                ended = False
            else:
                start = g["game_datetime"].split("T")[1]
                a,b = self.T_to_pdt(start)
                gamestart = datetime.time(hour=a, minute=b)
                curtime = datetime.datetime.now().time()
                st += f"{away} at {home}\n"
                if gamestart >= curtime:
                    st += f"Start time: {self.prettytime(a,b)}\n"
                else:
                    st += f"Delayed\n"
                ended = False
        if ended == False:
            st += f"Watch: {self.to_bilas(away.lower(), home.lower())}\n"
        await self.send(channel, st)


    async def cmd_41(self, user, channel, msg, ogcmd, *args):
        await channel.send("https://open.spotify.com/artist/5CKuMRGq5IzrLCa9m6ukj8")
        return
        if len(args) == 0:
            await channel.send("https://open.spotify.com/artist/5CKuMRGq5IzrLCa9m6ukj8")
        else:
            query = "%20".join(args)
            url = f'https://open.spotify.com/search/artist%3a%22fortyone%20savage%22%20track%3a%22{query}%22'
            await channel.send(url)
    async def cmd_ohgod(self, user, channel, msg, ogcmd, *args):
        await self.cmd_ohman(user, channel, msg, ogcmd, *args)
    async def cmd_ohman(self, user, channel, msg, ogcmd, *args):
        await channel.send("https://www.youtube.com/watch?v=8qloG5KG9oE")
    async def cmd_wes(self, user, channel, msg, ogcmd, *args):
        require(user, "manager")
        await channel.send(f"{emote('wes0')}")
    async def cmd_updatereplies(self, user, channel, msg, ogcmd, *args):
        require(user, "picture adder")
        self.update_replies()
        await channel.send(f"{emote('ezball')} replies updated")

    async def cmd_playerinfo(self, user, channel, msg, ogcmd, *args):
        if len(args) == 0:
            await self.send(channel, f"@{user}, usage is !playerinfo [player name]")
            return
        name = " ".join(args)
        pid = requests.get("http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'"
                f"&active_sw='Y'&name_part='{name}%'&search_player_all.col_in=player_id")
        jso = json.loads(pid.text)
        print(jso["search_player_all"]["queryResults"]["row"]["player_id"])

    async def cmd_benspecial(self, user, channel, msg, ogcmd, *args):
        msg  = "Ingredients: grilled chicken, hamburger, rice, sriracha, tapatio,\n"
        msg += "                       soy sauce, bbq sauce, garlic powder, black pepper\n"
        msg += "Literally chop up meats and mix everything"
        await channel.send(msg)
    async def cmd_8ball(self, user, channel, msg, ogcmd, *args):
        c = ["It is Certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.",
                "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
                "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
                "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
                "Don't count on it.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Very doubtful."]
        msg = random.choice(c)
        await self.send(channel, msg)

    async def cmd_points(self, user, channel, msg, ogcmd, *args):
        await self.send(channel, f"@{user}, you have {self.points[user.name]} points.\nYou can get more by sending messages.")

    def updatepoints(self):
        with open("points.txt", "w") as pf:
            for u,p in self.points.items():
                pf.write(f"{u}\t{p}\n")
        print(self.points)
    async def cmd_odds(self, user, channel, msg, ogcmd, *args):
        msg = f"@{user}, odds for !gamble are\n"
        msg += "     0.5% - 100x\n"
        msg += "     4.5% - 10x\n"
        msg += "     20%  - 2x\n"
        msg += "     25%  - 1.2x\n"
        msg += "     50%  - 0x"
        await self.send(channel, msg)
        
        
    async def cmd_gamble(self, user, channel, msg, ogcmd, *args):
        if len(args) != 1:
            await self.send(channel, f"@{user}, usage is !gamble [amount]")
            return
        u = user.name
        amt = 0
        if args[0] == "all":
            amt = self.points[u]
        elif args[0][-1] == "%":
            p = args[0][:-1]
            try:
                p = float(p)
            except ValueError:
                await self.send(channel, f"@{user}, that is not a valid percentage.")
                return
            if p > 100:
                await self.send(channel, f"@{user}, you can't bet more than you have.")
                return
            elif p < 0:
                await self.send(channel, f"@{user}, you can't bet negative.")
                return

            amt = int(self.points[u]*p/100)
        else:
            try:
                amt = int(args[0])
            except ValueError:
                await self.send(channel, f"@{user}, that is not a valid quantity.")
                return
            if amt > self.points[u]:
                await self.send(channel,f"@{user}, you can't bet more than you have (you have {self.points[u]}).")
                return
            elif amt < 0:
                await self.send(channel, f"@{user}, you can't bet negative.")
                return
        if amt == 0:
            await self.send(channel, f"@{user}, betting nothing gets you nothing smh")
            return

        self.points[u] -= amt
        
        win = 0
        wmsg = f"@{user} gambled {amt} and "
        r = random.random()
        if r < 0.005:
            win = int(100*amt)
            wmsg += f"holy this guy's a :peepogamble: ing god, won {win} points, which is 100x their initial gamble! :peepogamble: :rain: :peeporocket:"
        elif r < 0.05:
            win = int(10*amt)
            wmsg += f"won {win}, which is 10x the gamble! Whaaat theeee :wes0:"
        elif r < 0.25:
            win = int(2*amt)
            wmsg += f"won {win}! That's a pretty good :peepogamble:"
        elif r < 0.50:
            win = int(1.2*amt)
            wmsg += f"got a 20% return, winning {win}... we take those. :stonks:"
        else:
            wmsg += "l :omegalul: s t them all! :kekw:"
        self.points[u] += win

        wmsg += f"\nThey now have {self.points[u]} points."
        await self.send(channel, wmsg)

        self.updatepoints()

    async def send(self, channel, message):
        m = re.findall( ":[a-zA-Z\d_]*:", message )
        p = re.split( ":[a-zA-Z\d_]*:", message )
        s = ""
        for i, ename in enumerate(m):
            ename = ename[1:-1]
            s += p[i]
            s += emote(ename)
        s += p[-1]
        await channel.send(s)
          
            
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        user = message.author


        if message.content.startswith('!'):
            cmd, *args = message.content.split()
            cmd = cmd[1:].lower()

            found = False
            try:
                await getattr(self, "cmd_" + cmd)(user, message.channel, message, cmd, *args)
                found = True
            except AttributeError:
                pass
            except NotAllowedException:
                await message.channel.send(f"@{user} you don't have permission to use that")

            if found == True:
                return

            if cmd in self.extracmds:
                nas = self.extracmds[cmd]["arg"]

                if len(args) not in nas:
                    await message.channel.send(f"!{cmd} requires {na} arguments")
                else:
                    for i in range(len(args)):
                        exec(f"a{i} = args[{i}]")
                    narg = len(args)

                    await message.channel.send(eval(f"f\"{self.extracmds[cmd]['msg']}\""))
            else:
                print(f"invalid command {cmd}")



        else:
            self.points[user.name] += 10
            content = message.content.lower()
            om = content.find("oh man")
            og = content.find("oh god")
            if om > og and om >= 0:
                await message.channel.send("oh god")
            elif om < og and og >= 0:
                await message.channel.send("oh man")
            else:
                for k,v in self.replies.items():
                    if content.find(k) >= 0:
                        await message.channel.send(eval(f"f'{v}'"))
            self.updatepoints()


class NotAllowedException(Exception):
    pass


def emote(name):
    for e in bot.client.emojis:
        if e.name == name:
            return f"<:{name}:{e.id}>"
    return name

def require(user, *roles):
    for r in roles:
        if has_role(user, r):
            return
    raise NotAllowedException

def has_role(user, role):
    for r in user.roles:
        if r.name.lower() == role.lower():
            return True
    return False

def is_manager(user):
    return has_role(user, "Manager")


bot = callbackwrapper()
emoteslist = bot.client.emojis

@bot.client.event
async def on_ready():
    await bot.on_ready()

@bot.client.event
async def on_message(message):
    await bot.on_message(message)
    

@tasks.loop(days=1)
async def announce_scheduled():
    await bot.announce("@everyone TEST this better be sent at 8AM")


@announce_scheduled.before_loop
async def announcement_scheduler():
    now = datetime.datetime.utcnow()  # or `utcnow`
    future = datetime.datetime(now.year, now.month, now.day, now.hour + 1, 0)
    WHEN = datetime.time(16, 0, 0)
    future = datetime.datetime.combine(now.date(), WHEN)
    delta = (future - now).total_seconds()

    await asyncio.sleep(delta)





bot.start()

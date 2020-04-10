import random

def desc_template():
	desc_no = random.randrange(1,10)
	if desc_no == 1:
		pass
	elif desc_no == 2:
		pass
	elif desc_no == 3:
		pass
	elif desc_no == 4:
		pass
	elif desc_no == 5:
		pass
	elif desc_no == 6:
		pass
	elif desc_no == 7:
		pass
	elif desc_no == 8:
		pass
	else:
		pass

def get_lore():
	desc_no = random.randrange(1,7)
	if desc_no == 1:
		return "Ein kleines Dorf in einem Wald wird unerwartet von Werwölfen heimgesucht. \nDie Dorfbewohner versuchen, die als Menschen getarnten Wölfe zu entlarven und aufzuhalten. \nWährenddessen wollen die Wölfe als einzige überleben und nachts einen Dorfbewohner nach dem anderen fressen."
	elif desc_no == 2:
		return "Wir befinden uns in in dem malerischen Dörfchen Düsterwald. Doch die Idylle trügt.\nSeit geraumer Zeit treibt ein Rudel Werwölfe sein Unwesen und jede Nacht fällt seinem unstillbaren Hunger ein Dorfbewohner zum Opfer.\nIn dem Bestreben, das Übel auszurotten, greifen die Dorfbewohner ihrerseits zur Selbsthilfe und der einst beschauliche Ort wird zur Bühne für ein erbittert geführten Kampf ums nackte Sein."
	elif desc_no == 3:
		return "Es war einmal ein kleines Dorf namens Düsterwald. \nFür den Außenstehenden scheint hier alles in Ordnung zu sein. Doch sobald die Nacht hereinbricht, wird es gefährlich auf den Straßen von Düsterwald und nicht mal in seinem eigenen Haus ist man sicher: Ein halbblinder Jäger liegt auf der Lauer, eine Hexe braut unbekannte Tränke und darüber hinaus treiben gefährliche Werwölfe ihr unwesen. \nEs geht ums reine Überleben. \nSelbst tagsüber findet das Dorf keine Ruhe: Um dem nächtlichen Spuk ein Ende zu bereiten, wird ein Bewohner nach dem anderen gelyncht und auch manch Unschuldiger findet dadurch seine letzte Ruhe..."
	elif desc_no == 4:
		return "Ein Ort: Düsterwald. Zwei Teams: Werwölfe und Dorfbewohner. Eine Mission: Als Gruppe zu überleben."
	elif desc_no == 5:
		return "Der Ort ist unwichtig. Die Zeit: irrelevant. Die Realität: vollständig subjektiv. Die Deduktionsfähigkeit: unabdingbar. Verluste: an der Tagesordnung. Das Ende: unausweichlich. Der Sieger: offen."
	else:
		return "Wir befinden uns im märchenhaften Dorf Düsterwald. \nNormale Dorfbewohner liefern sich erbitterte Kämpfe mit den sagenumwobenen Werwölfen, während sie Unterstützung von magischen Figuren wie der Hexe erhalten. \nEs geht nur um eines: nicht in die ewigen Jagdgründe einzugehen, sondern der eigenen Spezies zum Überleben zu verhelfen."

def description_dorfbewohner():
	desc_no = random.randrange(1,7)
	if desc_no == 1:
		return "Du bist Dorfbewohner, ein normaler Charakter mit keinerlei besonderen Fähigkeiten."
	elif desc_no == 2:
		return "Bei deiner Rolle handelt es sich um den Dorfbewohner, einem wehrlosen Charakter, der lediglich tagsüber abstimmen darf."
	elif desc_no == 3:
		return "Du bist ein normaler Dorfbewohner, dessen einzige Waffe die Demokratie am Tage ist."
	elif desc_no == 4:
		return "Dein Charakter ist ein braver Bürger."
	elif desc_no == 5:
		return "Du bist ein Dorfbewohner, welcher nachts einfach in Ruhe durchschlafen darf."
	else:
		return "Du bist ein normaler Dorfbewohner, welcher sein Überleben nur durch das lynchen der Werwölfe am Tage zu schützen weiß."

def description_dorfbewohnerin():
	desc_no = random.randrange(1,7)
	if desc_no == 1:
		return "Du bist Dorfbewohnerin, ein normaler Charakter mit keinerlei besonderen Fähigkeiten."
	elif desc_no == 2:
		return "Bei deiner Rolle handelt es sich um die Dorfbewohnerin, einem wehrlosen Charakter, der lediglich tagsüber abstimmen darf."
	elif desc_no == 3:
		return "Du bist eine normale Dorfbewohnerin, deren einzige Waffe die Demokratie am Tage ist."
	elif desc_no == 4:
		return "Dein Charakter ist eine brave Bürgerin."
	elif desc_no == 5:
		return "Du bist eine Dorfbewohnerin, welche nachts einfach in Ruhe durchschlafen darf."
	else:
		return "Du bist eine normale Dorfbewohnerin, welche ihr Überleben nur durch das lynchen der Werwölfe am Tage zu schützen weiß."

def description_jaeger():
	desc_no = random.randrange(1,7)
	if desc_no == 1:
		return "Du bist der Jäger: Sollte er zu Tode kommen, kann er einen letzten Schuss abgeben und einen Mitspieler mit ins Verderben reißen."
	elif desc_no == 2:
		return "Du bist der Jäger, welcher in seinem letzen Atemzug noch zum Gewehr greift, um einen beliebigen Mitspieler ins Jenseits zu befördern."
	elif desc_no == 3:
		return "Bei deinem Charakter handelt es sich um den Jäger, welcher als letzte Aktion vor seinem Tod noch einen Spieler erschießen muss."
	elif desc_no == 4:
		return "Du bist der Jäger. Wenn der Jäger stirbt, muss er noch einen Spieler seiner Wahl in den Tod mitnehmen."
	elif desc_no == 5:
		return "Du bist der Jäger. Scheidet der Jäger aus dem Spiel aus, feuert er in seinem letzten Atemzug noch einen Schuss ab, mit dem er einen Spieler seiner Wahl mit in den Tod reißt."
	else:
		return "Du bist der Jäger. Als dieser musst du direkt vor deinem Tod mit deiner Jagdwaffe einen anderen Bewohner des Dorfes erschießen."

def description_seherin():
	desc_no = random.randrange(1,7)
	if desc_no == 1:
		return "Du bist die Serin. Diese erwacht jede Nacht, sucht sich einen Bewohner aus und erfährt, ob dieser zu den Werwölfen gehört oder nicht."
	elif desc_no == 2:
		return "Du bist die Seherin. Die Seherin hat die Fähigkeit, jede Nacht über einen Mitspieler zu erfahren, ob dieser zu den Werwölfen gehört."
	elif desc_no == 3:
		return "Bei deinem Charakter handelt es sich um die Seherin. Jede Nacht darf erhält sie die Einsicht über einen Spieler, ob dieser zu den Werwölfen gehört."
	elif desc_no == 4:
		return "Du bist die Seherin. Die Seherin erwählt jede Nacht einen Spieler. Sie erfährt, ob dieser gut oder böse ist."
	elif desc_no == 5:
		return "Du bist die Seherin. Die Seherin erwacht, während alle anderen schlafen und darf sich eine Person aussuchen, über die sie erfahren will, ob diese gut oder böse ist. Da die Seherin zu jeder Runde die Gruppenzugehörigkeit einer weiteren Person im Spiel kennt, kann sie großen Einfluss nehmen, muss aber ihr Wissen vorsichtig einsetzen."
	else:
		return "Dein Charakter ist die Seherin. Als diese erhälst du die Fähigkeit, jede Nacht über eine ander Person zu erfahren, ob diese gut oder böse ist."

def description_hexe():
	desc_no = random.randrange(1,7)
	if desc_no == 1:
		return "Du bist die Hexe. Diese erwacht jede Nacht, erfährt das Opfer der Werwölfe und darf sich entscheiden, ob sie ihren einen Lebenstrank auf das Opfer anwendet. Anschließend hat sie die Möglichkeit, einmal im Spiel eine Person mit einem Todestrank zu ermorden."
	elif desc_no == 2:
		return "Du bist die Hexe. Ihr stehen zwei Tränke zur Verfügung, ein Heil- und ein Gifttrank. \nDeren Bedeutung ist zwar selbsterklärend, aber dennoch: Mit dem Gifttrank kann sie einmal im Spiel einen Mitspieler vergiften, mit dem Heiltrank jemanden vor den Werwölfen erretten (auch sich selber)."
	elif desc_no == 3:
		return "Deine Rolle ist die Hexe. Die Hexe erwacht immer direkt nachdem die Werwölfe ihr Opfer ausgesucht haben. Sie hat im Verlauf des gesamten Spiels einen Gift- und einen Heiltrank. Die Hexe erfährt das Mordopfer der Werwölfe und die Hexe kann diese mit ihrem Heiltrank heilen (auch sich selbst), so dass es am nächsten Morgen keinen Toten gibt. Sie kann aber auch den Gifttrank auf einen anderen Spieler anwenden; dann gibt es mehrere Tote."
	elif desc_no == 4:
		return "Dein Charakter ist die Hexe. Die Hexe bekommt jede Nacht das Opfer der Werwölfe angezeigt (sofern jemand durch die Werwölfe sterben würde) und kann einmal im Spiel das Opfer mit einem Heiltrank retten. Außerdem hat sie einen Todestrank, mit dem sie einmal im Spiel einen beliebigen Spieler töten kann."
	elif desc_no == 5:
		return "Du bist die Hexe. Ihr stehen im gesamten Spiel zwei verschiedene Tränke zur Auswahl: Sie darf einmal im Spiel, nachdem sie das Opfer der Werwölfe erfahren hat, dieses mit dem Lebenstrank retten und einmal im Spiel einen beliebigen Mitspieler mit einem Gifttrank aus dem Leben schießen."
	else:
		return "Bei deiner Rolle handelt es sich um die Hexe. Diese hat zwei Spezialfähigkeiten. Zum einen darf sie jede Nacht, sofern sie noch ihren einen Heiltrank besitzt, das Opfer der Werwölfe erfahren und ggf. heilen. Zum anderen darf sie einmal im Spiel Gift in das Getränk eines Mitspielers geben, welcher dann am nächsten Morgen nicht mehr erwacht."

def description_werwolf():
	desc_no = random.randrange(1,7)
	if desc_no == 1:
		return "Du bist einer der Werwölfe. Diese suchen sich jede Nacht gemeinsam ein Opfer aus, welches sie töten wollen. Ihr Ziel ist es, dass nur Charaktere der Werwölfe überleben."
	elif desc_no == 2:
		return "Du bist ein Werwolf. Jede Nacht zieht das Werwolfsrudel umher und sucht sich gemeinschaftlich ein Opfer aus, dass sie diese Nacht reißen wollen. Die Werwölfe gewinnen, falls alle Dorfbewohner gestorben sind."
	elif desc_no == 3:
		return "Du gehörst den Werwölfen an. Du suchst dir, zusammen mit den anderen Werwölfen jede Nacht deinen Mitternachtsimbiss aus."
	elif desc_no == 4:
		return "Du bist ein Werwolf, welcher sich jede Nacht mit seinem Wolfsrudel trifft, um sich einen Dorfbewohner zum snacken zu 'borgen'."
	elif desc_no == 5:
		return "Du bist ein Werwolf, welcher jede Nacht erwacht und sich ein Opfer unter den Dorfbewohnern sucht, um dieses dann gemeinsam mit den anderen Werwölfen anzugreifen."
	else:
		return "Du bist ein Werwolf. Da diese Rudeltiere sind, erwachen alle Werwölfe jede Nacht gemeinsam, um sich ein (hoffentlich) werloses Opfer unter den Dorfbewohnern zu suchen."

def inlineKey_werwolf_options(name):
	desc_no = random.randrange(0,10)
	if desc_no == 0:
		return (0, name + " reißen")
	elif desc_no == 1:
		return (1, name + " zu Gulasch verarbeiten")
	elif desc_no == 2:
		return (2,name + " als Geschnetzeltes genießen")
	elif desc_no == 3:
		return (3,name + " durch den Fleischwolf jagen")
	elif desc_no == 4:
		return (4,name + " den Hals umdrehen")
	elif desc_no == 5:
		return (5, name + " versnacken")
	elif desc_no == 6:
		return (6,name + " zur Stillung der Blutlust verwenden")
	elif desc_no == 7:
		return (7,name + " auf einen Mitternachtsimbiss treffen")
	elif desc_no == 8:
		return (8, name + " die Reißzähne in den Hals rammen")
	else:
		return (9, name + " mit einer Torte verwechseln")

def werwolf_response_options(option, name):
	if option == "0":
		return name + " zu reißen."
	elif option == "1":
		return name + " zu Gulasch zu verarbeiten."
	elif option == "2":
		return name + " als Geschnetzeltes zu genießen."
	elif option == "3":
		return name + " durch den Fleischwolf zu jagen."
	elif option == "4":
		return name + " den Hals umzudrehen."
	elif option == "5":
		return name + " zu versnacken."
	elif option == "6":
		return name + " zur Stillung der Blutlust zu verwenden."
	elif option == "7":
		return name + " auf einen Mitternachtsimbiss zu treffen."
	elif option == "8":
		return name + " die Reißzähne in den Hals zu rammen."
	else:
		return name + " mit einer Torte zu verwechseln."

def death_message():
	desc_no = random.randrange(1,16)
	if desc_no == 1:
		return " ist diese Nacht leider gestorben."
	elif desc_no == 2:
		return " erblickt das Licht des neuen Tages nicht mehr."
	elif desc_no == 3:
		return " wurde massakriert aufgefunden."
	elif desc_no == 4:
		return " existiert nur noch in Stücken."
	elif desc_no == 5:
		return " hat die letzten Stunden nicht überlebt."
	elif desc_no == 6:
		return " ist nicht mehr aufzufinden."
	elif desc_no == 7:
		return " war ein guter Kamerad."
	elif desc_no == 8:
		return " hat seinen letzten Kampf verloren."
	elif desc_no == 9:
		return " hat den Löffel abgegeben."
	elif desc_no == 10:
		return " besucht nun die ewigen Jagdgründe."
	elif desc_no == 11:
		return " hat leider ins Gras gebissen."
	elif desc_no == 12:
		return " wird nie wieder an den Freuden des Dorfes teilhaben."
	elif desc_no == 13:
		return " ist von uns gegangen."
	elif desc_no == 14:
		return " ist über die Wupper geganen."
	else: 
		return " hat das Zeitliche gesegnet."

def anklage_options():
	desc_no = random.randrange(1,7)
	if desc_no == 1:
		return (1," anklagen")
	elif desc_no == 2:
		return (2," bezichtigen")
	elif desc_no == 3:
		return (3," Verrat vorwerfen")
	elif desc_no == 4:
		return (4," anprangern")
	elif desc_no == 5:
		return (5," anschuldigen")
	else:
		return (6," beschuldigen")

def anklage_change(option, target_name):
	if option == "1":
		return " möchte nun " + target_name + " anklagen."
	elif option == "2":
		return " bezichtigt nun " + target_name + "."
	elif option == "3":
		return " wirft nun " + target_name + " Verrat vor!"
	elif option == "4":
		return " will nun " + target_name + " anprangern!"
	elif option == "5":
		return " trifft nun Anschuldigungen gegen " + target_name + "."
	else:
		return " beschuldigt jetzt " + target_name + "."

def anklage_new(option, target_name):
	if option == "1":
		return " klagt " + target_name + " an!"
	elif option == "2":
		return " bezichtigt " + target_name + "!"
	elif option == "3":
		return " wirft " + target_name + " Verrat vor."
	elif option == "4":
		return " prangert " + target_name + " an."
	elif option == "5":
		return " veräussert Anschuldigungen gegen " + target_name + " ."
	else:
		return " beschuldigt " + target_name + "."

def vote_options():
	desc_no = random.randrange(0,7)
	if desc_no == 0:
		return (0," hängen")
	elif desc_no == 1:
		return (1," auf dem Scheiterhaufen verbrennen")
	elif desc_no == 2:
		return (2," einen Schwedentrunk verabreichen")
	elif desc_no == 3:
		return (3," vierteilen")
	elif desc_no == 4:
		return (4," für das Gemeinwohl opfern")
	elif desc_no == 5:
		return (5," ertränken")
	elif desc_no == 6:
		return (6," von einem Felsen stürzen")
	elif desc_no == 7:
		return (7," guillotinieren")
	elif desc_no == 8:
		return (8," lebend begraben")
	else:
		return (9," steinigen")

def vote_new(option, target_name):
	if option == "0":
		return " möchte " + target_name + " hängen!"
	elif option == "1":
		return " will " + target_name + " auf dem Scheiterhaufen sehen!"
	elif option == "2":
		return " möchte " + target_name + " den Schwedentrunk verabreichen."
	elif option == "3":
		return " will " + target_name + " vierteilen."
	elif option == "4":
		return " würde gerne " + target_name + " für das Gemeinwohl opfern."
	elif option == "5":
		return " möchte " + target_name + " ertränken."
	elif option == "6":
		return " will " + target_name + " von einem Felsen stürzen."
	elif option == "7":
		return " will " + target_name + " unter die Guillotine legen."
	elif option == "8":
		return " würde gerne " + target_name + " lebendig begraben."
	else:
		return " will " + target_name + " steinigen."

def vote_change(option, target_name):
	if option == "0":
		return " möchte nun " + target_name + " hängen!"
	elif option == "1":
		return " will neuerdings " + target_name + " auf dem Scheiterhaufen sehen!"
	elif option == "2":
		return " möchte jetzt " + target_name + " den Schwedentrunk verabreichen."
	elif option == "3":
		return " hat nun vor, " + target_name + " zu vierteilen."
	elif option == "4":
		return " würde doch gerne " + target_name + " für das Gemeinwohl opfern."
	elif option == "5":
		return " möchte jetzt doch " + target_name + " ertränken."
	elif option == "6":
		return " will nun " + target_name + " von einem Felsen stürzen."
	elif option == "7":
		return " will jetzt doch " + target_name + " unter die Guillotine legen."
	elif option == "8":
		return " würde jetzt gerne " + target_name + " lebendig begraben."
	else:
		return " will nun doch " + target_name + " steinigen."

def vote_judgement(option):
	if option == "0":
		return " wurde gehängt."
	elif option == "1":
		return " wird auf dem Scheiterhaufen verbrannt!"
	elif option == "2":
		return " bekommt den Schwedentrunk verabreicht."
	elif option == "3":
		return " wurde gevierteilt."
	elif option == "4":
		return " hat sich für das Gemeinwohl opfern lassen."
	elif option == "5":
		return " wurde ertränkt!"
	elif option == "6":
		return " wird von einem Felsen gestürzt."
	elif option == "7":
		return " ist unter der Guillotine gelandet!"
	elif option == "8":
		return " wurde lebendig begraben."
	else:
		return " hat die Steinigung nicht überlebt."
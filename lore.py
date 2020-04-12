import random
import json
import requests

def get_lore():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Ein kleines Dorf in einem Wald wird unerwartet von Werwölfen heimgesucht. \nDie Dorfbewohner versuchen, die als Menschen getarnten Wölfe zu entlarven und aufzuhalten. \nWährenddessen wollen die Wölfe als einzige überleben und nachts einen Dorfbewohner nach dem anderen fressen."
	elif desc_no == 2: return "Wir befinden uns in dem malerischen Dörfchen Düsterwald. Doch die Idylle trügt.\nSeit geraumer Zeit treibt ein Rudel Werwölfe sein Unwesen und jede Nacht fällt seinem unstillbaren Hunger ein Dorfbewohner zum Opfer.\nIn dem Bestreben, das Übel auszurotten, greifen die Dorfbewohner ihrerseits zur Selbsthilfe und der einst beschauliche Ort wird zur Bühne für ein erbittert geführten Kampf ums nackte Sein."
	elif desc_no == 3: return "Es war einmal ein kleines Dorf namens Düsterwald. \nFür den Außenstehenden scheint hier alles in Ordnung zu sein. Doch sobald die Nacht hereinbricht, wird es gefährlich auf den Straßen von Düsterwald und nicht mal in seinem eigenen Haus ist man sicher: Ein halbblinder Jäger liegt auf der Lauer, eine Hexe braut unbekannte Tränke und darüber hinaus treiben gefährliche Werwölfe ihr unwesen. \nEs geht ums reine Überleben. \nSelbst tagsüber findet das Dorf keine Ruhe: Um dem nächtlichen Spuk ein Ende zu bereiten, wird ein Bewohner nach dem anderen gelyncht und auch manch Unschuldiger findet dadurch seine letzte Ruhe..."
	elif desc_no == 4: return "Ein Ort: Düsterwald. Zwei Teams: Werwölfe und Dorfbewohner. Eine Mission: Als Gruppe zu überleben."
	elif desc_no == 5: 	return "Der Ort ist unwichtig. Die Zeit: irrelevant. Die Realität: vollständig subjektiv. Die Deduktionsfähigkeit: unabdingbar. Verluste: an der Tagesordnung. Das Ende: unausweichlich. Der Sieger: offen."
	else: return "Wir befinden uns im märchenhaften Dorf Düsterwald. \nNormale Dorfbewohner liefern sich erbitterte Kämpfe mit den sagenumwobenen Werwölfen, während sie Unterstützung von magischen Figuren wie der Hexe erhalten. \nEs geht nur um eines: nicht in die ewigen Jagdgründe einzugehen, sondern der eigenen Spezies zum Überleben zu verhelfen."

def description_dorfbewohner():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist Dorfbewohner, ein normaler Charakter mit keinerlei besonderen Fähigkeiten."
	elif desc_no == 2: return "Bei deiner Rolle handelt es sich um den Dorfbewohner, einem wehrlosen Charakter, der lediglich tagsüber abstimmen darf."
	elif desc_no == 3: return "Du bist ein normaler Dorfbewohner, dessen einzige Waffe die Demokratie am Tage ist."
	elif desc_no == 4: return "Dein Charakter ist ein braver Bürger."
	elif desc_no == 5: return "Du bist ein Dorfbewohner, welcher nachts einfach in Ruhe durchschlafen darf."
	else: return "Du bist ein normaler Dorfbewohner, welcher sein Überleben nur durch das Lynchen der Werwölfe am Tage zu schützen weiß."

def description_dorfbewohnerin():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist Dorfbewohnerin, ein normaler Charakter mit keinerlei besonderen Fähigkeiten."
	elif desc_no == 2: return "Bei deiner Rolle handelt es sich um die Dorfbewohnerin, einem wehrlosen Charakter, der lediglich tagsüber abstimmen darf."
	elif desc_no == 3: return "Du bist eine normale Dorfbewohnerin, deren einzige Waffe die Demokratie am Tage ist."
	elif desc_no == 4: return "Dein Charakter ist eine brave Bürgerin."
	elif desc_no == 5: return "Du bist eine Dorfbewohnerin, welche nachts einfach in Ruhe durchschlafen darf."
	else: return "Du bist eine normale Dorfbewohnerin, welche ihr Überleben nur durch das Lynchen der Werwölfe am Tage zu schützen weiß."

def description_jaeger():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist der Jäger: Sollte er zu Tode kommen, kann er einen letzten Schuss abgeben und einen Mitspieler mit ins Verderben reißen."
	elif desc_no == 2: return "Du bist der Jäger, welcher in seinem letzen Atemzug noch zum Gewehr greift, um einen beliebigen Mitspieler ins Jenseits zu befördern."
	elif desc_no == 3: return "Bei deinem Charakter handelt es sich um den Jäger, welcher als letzte Aktion vor seinem Tod noch einen Spieler erschießen muss."
	elif desc_no == 4: return "Du bist der Jäger. Wenn der Jäger stirbt, muss er noch einen Spieler seiner Wahl in den Tod mitnehmen."
	elif desc_no == 5: return "Du bist der Jäger. Scheidet der Jäger aus dem Spiel aus, feuert er in seinem letzten Atemzug noch einen Schuss ab, mit dem er einen Spieler seiner Wahl mit in den Tod reißt."
	else: return "Du bist der Jäger. Als dieser musst du direkt vor deinem Tod mit deiner Jagdwaffe einen anderen Bewohner des Dorfes erschießen."

def description_rotkaeppchen():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist das Rotkäppchen. Solange der Jäger am Leben ist, bleibt das Rotkäppchen nachts immun gegen normale Angriffe von Werwölfen."
	elif desc_no == 2: return "Deine Rolle ist das Rotkäppchen, welches nachts nicht von den Werwölfen gerissen werden kann, solange der Jäger noch lebt."
	elif desc_no == 3: return "Du bist das Rotkäppchen. Dieses wird nachts vom Jäger, solange dieser lebt, vor Werwölfen beschützt."
	elif desc_no == 4: return "Dein Charakter ist das Rotkäppchen, welches unter dem Schutz des Jägers steht, solange dieser lebt. Dies bedeutet, dass solange der Jäger lebt, das Rotkäppchen nicht nachts durch Werwölfe getötet werden kann."
	elif desc_no == 5: return "Du bist das märchenhafte Rotkäppchen, welches zu Lebzeiten des Jägers von diesem vor Werwolfangriffen geschützt wird."
	else: return "Du bist das Rotkäppchen, welches nicht durch Werwolfangriffe sterben kann, solange der Jäger lebt."

def description_wolfshund():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist der Wolfshund. Als dieser darfst du in der ersten Nacht entscheiden, ob du das Spiel als Werwolf oder als Dorfbewohner spielen willst."
	elif desc_no == 2: return "Du bist ein Wolfshund, welcher sowohl die Gene eines friedlichen Hundes als auch die eines Wolfes in sich hat. Er entscheidet sich in der ersten Nacht, ob er zum Dorf oder zu den Werwölfen gehören will."
	elif desc_no == 3: return "Deine Rolle ist der Wolfshund. Der Wolfshund entscheidet sich in der ersten Nacht, ob er zu den Dorfbewohnern oder zu den Werwölfen gehören will."
	elif desc_no == 4: return "Dein Charakter ist der Wolfshund, welcher in der ersten Nacht vor den Werwölfen erwacht und sich entscheiden muss, ob er zu den Werwölfen oder zum Dorf gehört."
	elif desc_no == 5: return "Du bist der Wolfshund. Der Wolfshund hat die Wahl, ob er das Spiel als Werwolf oder Dorfbewohner bestreiten will."
	else: return "Du bist der Wolfshund und besitzt die Fähigkeit, dich zu Beginn des Spieles zu entscheiden, ob du ein Dorfbewohner oder ein Werwolf wirst."

def description_seherin():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist die Seherin. Diese erwacht jede Nacht, sucht sich einen Bewohner aus und erfährt, ob dieser zu den Werwölfen gehört oder nicht."
	elif desc_no == 2: return "Du bist die Seherin. Die Seherin hat die Fähigkeit, jede Nacht über einen Mitspieler zu erfahren, ob dieser zu den Werwölfen gehört."
	elif desc_no == 3: return "Bei deinem Charakter handelt es sich um die Seherin. Jede Nacht erhält sie Einsicht über einen Spieler, ob dieser zu den Werwölfen gehört."
	elif desc_no == 4: return "Du bist die Seherin. Die Seherin erwählt jede Nacht einen Spieler. Sie erfährt, ob dieser gut oder böse ist."
	elif desc_no == 5: return "Du bist die Seherin. Die Seherin erwacht, während alle anderen schlafen und darf sich eine Person aussuchen, über die sie erfahren will, ob diese gut oder böse ist. Da die Seherin zu jeder Runde die Gruppenzugehörigkeit einer weiteren Person im Spiel kennt, kann sie großen Einfluss nehmen, muss aber ihr Wissen vorsichtig einsetzen."
	else: return "Dein Charakter ist die Seherin. Als diese erhälst du die Fähigkeit, jede Nacht über eine ander Person zu erfahren, ob diese gut oder böse ist."

def description_hexe():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist die Hexe. Diese erwacht jede Nacht, erfährt das Opfer der Werwölfe und darf sich entscheiden, ob sie ihren einen Lebenstrank auf das Opfer anwendet. Anschließend hat sie die Möglichkeit, einmal im Spiel eine Person mit einem Todestrank zu ermorden."
	elif desc_no == 2: return "Du bist die Hexe. Ihr stehen zwei Tränke zur Verfügung, ein Heil- und ein Gifttrank. \nDeren Bedeutung ist zwar selbsterklärend, aber dennoch: Mit dem Gifttrank kann sie einmal im Spiel einen Mitspieler vergiften, mit dem Heiltrank jemanden vor den Werwölfen erretten (auch sich selber)."
	elif desc_no == 3: return "Deine Rolle ist die Hexe. Die Hexe erwacht immer direkt nachdem die Werwölfe ihr Opfer ausgesucht haben. Sie hat im Verlauf des gesamten Spiels einen Gift- und einen Heiltrank. Die Hexe erfährt das Mordopfer der Werwölfe und kann dieses mit ihrem Heiltrank heilen (auch sich selbst), so dass es am nächsten Morgen keinen Toten gibt. Sie kann aber auch den Gifttrank auf einen anderen Spieler anwenden; dann gibt es mehrere Tote."
	elif desc_no == 4: return "Dein Charakter ist die Hexe. Die Hexe bekommt jede Nacht das Opfer der Werwölfe angezeigt (sofern jemand durch die Werwölfe sterben würde) und kann einmal im Spiel das Opfer mit einem Heiltrank retten. Außerdem hat sie einen Todestrank, mit dem sie einmal im Spiel einen beliebigen Spieler töten kann."
	elif desc_no == 5: return "Du bist die Hexe. Ihr stehen im gesamten Spiel zwei verschiedene Tränke zur Auswahl: Sie darf einmal im Spiel, nachdem sie das Opfer der Werwölfe erfahren hat, dieses mit dem Lebenstrank retten und einmal im Spiel einen beliebigen Mitspieler mit einem Gifttrank aus dem Leben schießen."
	else: return "Bei deiner Rolle handelt es sich um die Hexe. Diese hat zwei Spezialfähigkeiten. Zum einen darf sie jede Nacht, sofern sie noch ihren einen Heiltrank besitzt, das Opfer der Werwölfe erfahren und ggf. heilen. Zum anderen darf sie einmal im Spiel Gift in das Getränk eines Mitspielers geben, welcher dann am nächsten Morgen nicht mehr erwacht."

def description_werwolf():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist einer der Werwölfe. Diese suchen sich jede Nacht gemeinsam ein Opfer aus, welches sie töten wollen. Ihr Ziel ist es, dass nur Charaktere der Werwölfe überleben."
	elif desc_no == 2: return "Du bist ein Werwolf. Jede Nacht zieht das Werwolfsrudel umher und sucht sich gemeinschaftlich ein Opfer aus, dass sie diese Nacht reißen wollen. Die Werwölfe gewinnen, falls alle Dorfbewohner gestorben sind."
	elif desc_no == 3: return "Du gehörst den Werwölfen an. Du suchst dir, zusammen mit den anderen Werwölfen jede Nacht deinen Mitternachtsimbiss aus."
	elif desc_no == 4: return "Du bist ein Werwolf, welcher sich jede Nacht mit seinem Wolfsrudel trifft, um sich einen Dorfbewohner zum snacken zu 'borgen'."
	elif desc_no == 5: return "Du bist ein Werwolf, welcher jede Nacht erwacht und sich ein Opfer unter den Dorfbewohnern sucht, um dieses dann gemeinsam mit den anderen Werwölfen anzugreifen."
	else: return "Du bist ein Werwolf. Da diese Rudeltiere sind, erwachen alle Werwölfe jede Nacht gemeinsam, um sich ein (hoffentlich) werloses Opfer unter den Dorfbewohnern zu suchen."

def description_harter_bursche():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist der Harte Bursche. Der Harte Bursche überlebt den ersten Werwolf-Angriff."
	elif desc_no == 2: return "Du bist ein harter Bursche. Also so richtig hart. Du überlebst sogar einen Werwolfangriff. Aber nur den ersten."
	elif desc_no == 3: return "Deine Rolle ist der Harte Bursche. Dieser überlebt durch seine männliche Härte und Kraft den ersten Werwolfangriff."
	elif desc_no == 4: return "Dein Charakter ist der Harte Bursche. Dieser hat die Fähigkeit, sich gegen den ersten Werwolfangriff zu verteidigen. Gegen andere Gefahren wie die Hexe oder die Hinrichtung hilft deine Härte aber Nichts."
	elif desc_no == 5: return "Du bist ein harter Bursche. Muskeln aus Stahl, breiter als der Türsteher. Damit kannst du den ersten Angriff der Werwölfe erfolgreich abwenden."
	else: return "Du bist ein harter Bursche. Nein, du bist DER Harte Bursche von Düsterwald. Hart genug, um den ersten Werwolfangriff zu überleben, aber nicht hart genug, um dem Gift der Hexe oder der Hinrichtung des Dorfes zu standzuhalten."

def inlineKey_werwolf_options(name):
	desc_no = random.randrange(0,12)
	if desc_no == 0: return (0, name + " reißen")
	elif desc_no == 1: return (1, name + " zu Gulasch verarbeiten")
	elif desc_no == 2: return (2,name + " als Geschnetzeltes genießen")
	elif desc_no == 3: return (3,name + " durch den Fleischwolf jagen")
	elif desc_no == 4: return (4,name + " den Hals umdrehen")
	elif desc_no == 5: return (5, name + " versnacken")
	elif desc_no == 6: return (6,name + " zur Stillung der Blutlust verwenden")
	elif desc_no == 7: return (7,name + " auf einen Mitternachtsimbiss treffen")
	elif desc_no == 8: return (8, name + " die Reißzähne in den Hals rammen")
	elif desc_no == 9: return (9, name + " zu Salami verarbeiten")
	elif desc_no == 10: return (10, name + " in die Lasagne mischen")
	else: return (11, name + " mit einer Torte verwechseln")

def werwolf_response_options(option, name):
	if option == "0": return name + " zu reißen."
	elif option == "1": return name + " zu Gulasch zu verarbeiten."
	elif option == "2": return name + " als Geschnetzeltes zu genießen."
	elif option == "3": return name + " durch den Fleischwolf zu jagen."
	elif option == "4": return name + " den Hals umzudrehen."
	elif option == "5": return name + " zu versnacken."
	elif option == "6": return name + " zur Stillung der Blutlust zu verwenden."
	elif option == "7": return name + " auf einen Mitternachtsimbiss zu treffen."
	elif option == "8": return name + " die Reißzähne in den Hals zu rammen."
	elif option == "9": return name + " zu Salami zu verarbeiten."
	elif option == "10": return name + " in die Lasagne zu mischen."
	else: return name + " mit einer Torte zu verwechseln."

def death_message():
	desc_no = random.randrange(1,16)
	if desc_no == 1: return " ist diese Nacht leider gestorben."
	elif desc_no == 2: return " erblickt das Licht des neuen Tages nicht mehr."
	elif desc_no == 3: return " wurde massakriert aufgefunden."
	elif desc_no == 4: return " existiert nur noch in Stücken."
	elif desc_no == 5: return " hat die letzten Stunden nicht überlebt."
	elif desc_no == 6: return " ist nicht mehr aufzufinden."
	elif desc_no == 7: return " war ein guter Kamerad."
	elif desc_no == 8: return " hat seinen letzten Kampf verloren."
	elif desc_no == 9: return " hat den Löffel abgegeben."
	elif desc_no == 10: return " besucht nun die ewigen Jagdgründe."
	elif desc_no == 11: return " hat leider ins Gras gebissen."
	elif desc_no == 12: return " wird nie wieder an den Freuden des Dorfes teilhaben."
	elif desc_no == 13: return " ist von uns gegangen."
	elif desc_no == 14: return " ist über die Wupper gegangen."
	else:  return " hat das Zeitliche gesegnet."

def anklage_options():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return (1," anklagen")
	elif desc_no == 2: return (2," bezichtigen")
	elif desc_no == 3: return (3," Verrat vorwerfen")
	elif desc_no == 4: return (4," anprangern")
	elif desc_no == 5: return (5," anschuldigen")
	else: return (6," beschuldigen")

def anklage_change(option, target_name):
	if option == "1": return " möchte nun " + target_name + " anklagen."
	elif option == "2": return " bezichtigt nun " + target_name + "."
	elif option == "3": return " wirft nun " + target_name + " Verrat vor!"
	elif option == "4": return " will nun " + target_name + " anprangern!"
	elif option == "5": return " trifft nun Anschuldigungen gegen " + target_name + "."
	else: return " beschuldigt jetzt " + target_name + "."

def anklage_new(option, target_name):
	if option == "1": return " klagt " + target_name + " an!"
	elif option == "2": return " bezichtigt " + target_name + "!"
	elif option == "3": return " wirft " + target_name + " Verrat vor."
	elif option == "4": return " prangert " + target_name + " an."
	elif option == "5": return " veräussert Anschuldigungen gegen " + target_name + " ."
	else: return " beschuldigt " + target_name + "."

def vote_options():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return (0," hängen")
	elif desc_no == 1: return (1," auf dem Scheiterhaufen verbrennen")
	elif desc_no == 2: return (2," einen Schwedentrunk verabreichen")
	elif desc_no == 3: return (3," vierteilen")
	elif desc_no == 4: return (4," für das Gemeinwohl opfern")
	elif desc_no == 5: return (5," ertränken")
	elif desc_no == 6: return (6," von einem Felsen stürzen")
	elif desc_no == 7: return (7," guillotinieren")
	elif desc_no == 8: return (8," lebend begraben")
	else: return (9," steinigen")

def vote_new(option, target_name):
	if option == "0": return " möchte " + target_name + " hängen!"
	elif option == "1": return " will " + target_name + " auf dem Scheiterhaufen sehen!"
	elif option == "2": return " möchte " + target_name + " den Schwedentrunk verabreichen."
	elif option == "3": return " will " + target_name + " vierteilen."
	elif option == "4": return " würde gerne " + target_name + " für das Gemeinwohl opfern."
	elif option == "5": return " möchte " + target_name + " ertränken."
	elif option == "6": return " will " + target_name + " von einem Felsen stürzen."
	elif option == "7": return " will " + target_name + " unter die Guillotine legen."
	elif option == "8": return " würde gerne " + target_name + " lebendig begraben."
	else: return " will " + target_name + " steinigen."

def vote_change(option, target_name):
	if option == "0": return " möchte nun " + target_name + " hängen!"
	elif option == "1": return " will neuerdings " + target_name + " auf dem Scheiterhaufen sehen!"
	elif option == "2": return " möchte jetzt " + target_name + " den Schwedentrunk verabreichen."
	elif option == "3": return " hat nun vor, " + target_name + " zu vierteilen."
	elif option == "4": return " würde doch gerne " + target_name + " für das Gemeinwohl opfern."
	elif option == "5": return " möchte jetzt doch " + target_name + " ertränken."
	elif option == "6": return " will nun " + target_name + " von einem Felsen stürzen."
	elif option == "7": return " will jetzt doch " + target_name + " unter die Guillotine legen."
	elif option == "8": return " würde jetzt gerne " + target_name + " lebendig begraben."
	else: return " will nun doch " + target_name + " steinigen."

def vote_judgement(option):
	if option == "0": return " wurde gehängt."
	elif option == "1": return " wird auf dem Scheiterhaufen verbrannt!"
	elif option == "2": return " bekommt den Schwedentrunk verabreicht."
	elif option == "3": return " wurde gevierteilt."
	elif option == "4": return " hat sich für das Gemeinwohl opfern lassen."
	elif option == "5": return " wurde ertränkt!"
	elif option == "6": return " wird von einem Felsen gestürzt."
	elif option == "7": return " ist unter der Guillotine gelandet!"
	elif option == "8": return " wurde lebendig begraben."
	else: return " hat die Steinigung nicht überlebt."

def inlineKey_jaeger_options():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return (0," erschießen")
	elif desc_no == 1: return (1," mit der Nagelpistole an die Wand heften")
	elif desc_no == 2: return (2," durchlöchern")
	elif desc_no == 3: return (3," umlegen")
	elif desc_no == 4: return (4," wegpusten")
	elif desc_no == 5: return (5," in der Notwehr erschießen")
	elif desc_no == 6: return (6," niederstrecken")
	elif desc_no == 7: return (7," zur Jagdtrophäe befördern")
	elif desc_no == 8: return (8," mit in den Tod reißen")
	else: return (9," einen Gnadenschuss verpassen")

def jaeger_shot(option):
	if option == "0": return " wurde vom Jäger erschossen"
	elif option == "1": return " wurde mit einer Nagelpistole an die Wand geheftet!"
	elif option == "2": return " hat nun sehr viele Löcher in Kopf und Brust."
	elif option == "3": return " wurde umgelegt."
	elif option == "4": return " hat sich wegpusten lassen."
	elif option == "5": return " wurde in der Notwehr des Jägers erschossen!"
	elif option == "6": return " wurde niedergestreckt."
	elif option == "7": return " endete als letzte Jagdtrophäe des Jägers!"
	elif option == "8": return " wurde vom Jäger mit in den Tod gerissen."
	else: return " hat einen Gnadenschuss erhalten."

def seherin_options(name):
	desc_no = random.randrange(0,7)
	if desc_no == 0: return (0,name + " einsehen")
	elif desc_no == 1: return (1,name + " von der Gestapo überwachen lassen")
	elif desc_no == 2: return (2,"Informationen über " + name + " beim BND einholen")
	elif desc_no == 3: return (3,name + " bespitzeln")
	elif desc_no == 4: return (4,name + " beobachten")
	elif desc_no == 5: return (5,"Ein Auge auf " + name + " werfen")
	else: return (6,name + " ausspionieren")

def seherin_werwolf(option, name):
	if option == "0": return name + " gehört zu den Werwölfen."
	elif option == "1": return "Die Gestapo hat herausgefunden: " + name + " ist ein Werwolf."
	elif option == "2": return "Der BND steckt dir zu: " + name + " ist böse!"
	elif option == "3": return name + " ist böse."
	elif option == "4": return "Es stellt sich heraus: " + name + " gehört den Bösen an."
	elif option == "5": return "Du siehst es mit deinen eigenen Augen: " + name + " verwandelt sich Nachts in einen Werwolf!"
	else: return "Deine Ermittlungen haben ergeben: " + name + " ist ein Werwolf."

def seherin_no_werwolf(option, name):
	if option == "0": return name + " gehört nicht zu den Werwölfen."
	elif option == "1": return "Die Gestapo hat herausgefunden: " + name + " ist kein Werwolf."
	elif option == "2": return "Der BND steckt dir zu: " + name + " ist gut!"
	elif option == "3": return name + " ist gut."
	elif option == "4": return "Es stellt sich heraus: " + name + " gehört den Guten an."
	elif option == "5": return "Du siehst es mit deinen eigenen Augen: " + name + " verwandelt sich Nachts nicht in einen Werwolf!"
	else: return "Deine Ermittlungen haben ergeben: " + name + " ist kein Werwolf."

def hexe_save():
	desc_no = random.randrange(0,6)
	if desc_no == 0: return "Retten"
	elif desc_no == 1: return "Heilen"
	elif desc_no == 2: return "Einen Lebenstrank verabreichen"
	elif desc_no == 3: return "Erfolgreich die Verletzungen versorgen"
	elif desc_no == 4: return "Wiederbeleben"
	else: return "Wieder zusammennähen"

def hexe_let_die():
	desc_no = random.randrange(0,8)
	if desc_no == 0: return "Sterben lassen"
	elif desc_no == 1: return "Nicht beachten"
	elif desc_no == 2: return "Dem Schicksal überlassen"
	elif desc_no == 3: return "Ausversehen zu spät kommen"
	elif desc_no == 4: return "Lieber schlafen"
	elif desc_no == 5: return "Umdrehen und weiterschlafen"
	elif desc_no == 6: return "Lebenstrank nicht für sojemanden verschwenden"
	else: return "Eigensicherung vorziehen"

def hexe_kill():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return " vergiften"
	elif desc_no == 1: return " den Todestrank einflößen"
	elif desc_no == 2: return " eine ungesunde Substanz injezieren"
	elif desc_no == 3: return " ausversehen eine Überdosis Morphium verabreichen"
	elif desc_no == 4: return " mit radioaktivem Gemüse versorgen"
	elif desc_no == 5: return "s innere Organe verätzen"
	elif desc_no == 6: return " ausversehen Gift in das Getränk mischen"
	elif desc_no == 7: return " ein Essen mit Fliegenpilzen zubereiten"
	elif desc_no == 8: return " einen Kugelfisch falsch zubereiten"
	else: return " Quecksilber in die Milch mischen"

def all_dead():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Es sind alle tot."
	elif desc_no == 1: return "Das Dorf ist so lebendig wie Tschernobyl."
	elif desc_no == 2: return "In Düsterwald könnte jetzt ein Vulkan ausbrechen und niemand würde sterben."
	elif desc_no == 3: return "Düsterwald hat seine Letzte Ruhe gefunden."
	elif desc_no == 4: return "Jetzt leben nur noch Tiere in Düsterwald."
	elif desc_no == 5: return "Die Natur wird sich das kleine Örtchen ab jetzt Stück für Stück zurückholen."
	elif desc_no == 6: return "Die Zivilisation in Düsterwald ist ausgelöscht."
	elif desc_no == 7: return "Das Werwolfproblem ist beseitigt. Das Menschenproblem aber auch."
	elif desc_no == 8: return "Düsterwald hat jetzt " + str(json.loads(requests.get("http://api.open-notify.org/astros.json").text)["number"]) + " Einwohner weniger als das Weltall!"
	else: return "Das Kapitel 'Düsterwald' ist jetzt endgültig abgeschlossen."

def werwoelfe_win():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Die Werwölfe gewinnen."
	elif desc_no == 1: return "Es war ein langer Kampf, aber die Werwölfe haben sich durchgesetzt."
	elif desc_no == 2: return "Es leben nur noch Werwölfe in Düsterwald!"
	elif desc_no == 3: return "Es gibt keine Dorfbewohner mehr, die von den Werwölfen verspeißt werden können."
	elif desc_no == 4: return "Es wird wieder friedlich in Düsterwald, da hier jetzt nur noch Werwölfe leben."
	elif desc_no == 5: return "Die Werwölfe haben gesiegt."
	elif desc_no == 6: return "Die Werwölfe haben ihre Dominanz bewiesen."
	elif desc_no == 7: return "Die Werwölfe sind in Düsterwald anscheinend die stärkere Rasse."
	elif desc_no == 8: return "Mit dem Tod des letzten Dorfbewohners haben die Werwölfe jetzt ihre Ruhe."
	else: return "Die Werwölfe veranstalten zur Feier des Tages einen Fest und verspeißen genussvoll den letzten Dorfbewohner."

def dorf_win():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Das Dorf gewinnt."
	elif desc_no == 1: return "Es war ein langer Kampf, aber die Dorfbewohner haben sich durchgesetzt."
	elif desc_no == 2: return "Es leben keine Werwölfe mehr in Düsterwald!"
	elif desc_no == 3: return "Es gibt keine Werwölfe mehr, die Dorfbewohner verspeißen wollen."
	elif desc_no == 4: return "Es wird wieder friedlich in Düsterwald, da hier nur noch Dorfbewohner leben."
	elif desc_no == 5: return "Die Dorfbewohner haben gesiegt."
	elif desc_no == 6: return "Die Dorfbewohner haben ihre Dominanz bewiesen."
	elif desc_no == 7: return "Die Werwölfe sind in Düsterwald anscheinend die unterlegene Rasse."
	elif desc_no == 8: return "Mit dem Tod des letzten Werwolfes haben die Dorfbewohner jetzt ihre Ruhe."
	else: return "Die Dorfbewohner veranstalten zur Feier des Tages einen Fest und stopfen den letzten Werwolf aus."

def lonely_wolf():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Du bist der einzige Werwolf."
	elif desc_no == 1: return "Als einsamer Werwolf streifst du durch das Dorf."
	elif desc_no == 2: return "Man nennt dich auch 'lonely wolf'."
	elif desc_no == 3: return "Du bist der letzte lebende Werwolf."
	elif desc_no == 4: return "Wenn du stirbst, sind die Werwölfe ausgestorben."
	elif desc_no == 5: return "Du bist der einzige Vertreter der Werwölfe."
	elif desc_no == 6: return "Du streifst mit deinem ganzen Rudel durch das Dorf. Du schaust dich um. Du bist alleine."
	elif desc_no == 7: return "Du fühlst dich einsam: du hast keine Werwolffreunde und das Dorf will dich häuten."
	elif desc_no == 8: return "Als einsamer Werwolf kämpfst du verzweifelt ums überleben."
	else: return "Du bist der 'Last Wolf Standing'."

def werwolf_choose_target():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Die Werwölfe suchen ihr Opfer aus."
	elif desc_no == 1: return "Das Werwolfsrudel streift hungrig durch das Dorf, auf der Suche nach einem Imbiss."
	elif desc_no == 2: return "Die Werwölfe erinnern sich an einen weisen Spruch: 'Wählt weise, denn jede Mahlzeit könnte eure letzte sein'."
	elif desc_no == 3: return "Auf der Suche nach Essen durchsuchen die Werwölfe das Dorf."
	elif desc_no == 4: return "Es ist Nacht. Es ist Mitternacht. Es ist Essenzeit!"
	elif desc_no == 5: return "Zu Tische, Werwölfe!"
	elif desc_no == 6: return "Auf wen die Werwölfe heute Nacht wohl Appetit haben?"
	elif desc_no == 7: return "Werwölfe, sucht euer Opfer aus!"
	elif desc_no == 8: return "Mit wem lassen sich die hungrigen Werwolfsmäuler am besten stopfen?"
	else: return "Die Werwolfsmägen knurren vor Hunger - Zeit, sich etwas zu Essen zu suchen!"

def jaeger_reveal():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return " war der Jäger!"
	elif desc_no == 1: return " schießt rücksichtslos, um nicht alleine sterben zu müssen!"
	elif desc_no == 2: return " trägt eine geladene Waffe bei sich!"
	elif desc_no == 3: return " zückt eine Schrotflinte!"
	elif desc_no == 4: return " versucht mit Waffengewalt, kurz vor seinem Tod noch für Gerechtigkeit zu sorgen!"
	elif desc_no == 5: return " hat einen Jagdschein!"
	elif desc_no == 6: return " hat eine Jagdlizenez. Jetzt auch für Menschen!"
	elif desc_no == 7: return " will nicht alleine sterben und zieht einen Revolver!"
	elif desc_no == 8: return " genießt es, jemanden zu sehen - und erschießt ihn!"
	else: return " fordert sein Recht ein - jemanden mit Waffengewalt in den Tod mitzunehmen."

def jaeger_choose_target():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Wen möchtest du mit ins Grab nehmen?"
	elif desc_no == 1: return "Wen möchtest du erschießen?"
	elif desc_no == 2: return "Wen willst du wegpusten?"
	elif desc_no == 3: return "Wen willst du in Notwehr abknallen?"
	elif desc_no == 4: return "Wen willst du ausversehen mit 15 Schüssen in der Brust treffen?"
	elif desc_no == 5: return "Wen möchtest du mit Blei ausstopfen?"
	elif desc_no == 6: return "Wem möchtest du zu einer inneren Bleivergiftung verhelfen?"
	elif desc_no == 7: return "Wen willst du als letzten Akt erschießen?"
	elif desc_no == 8: return "Wem gönnst du es nicht, ohne dich weiterzuleben?"
	else: return "Wer soll im Kugelhagel seine ewige Ruhe finden?"

def seherin_choose_target():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Die Seherin erwacht. Was wird sie tun?"
	elif desc_no == 1: return "Die Seherin schreckt aus dem Schlaf hoch. Über wen wird sie diese Nacht ein Geheimnis herrausfinden?"
	elif desc_no == 2: return "Die Seherin erwacht aus einem Albtraum. Sie hat eine Runden 'Ich sehe was, was du nicht siehst!' verloren. Das wird ihr jetzt nicht passieren!"
	elif desc_no == 3: return "Der Wecker der Seherin klingelt. Über wen will sie nun bespitzeln?"
	elif desc_no == 4: return "Die Seherin erwacht wie von einem Blitz getroffen. Wessen Geheimnis will sie diese Nacht lüften?"
	elif desc_no == 5: return "Als die Seherin nachts aufwacht, verspürt sie starken Tatendrang - was wird sie damit machen?"
	elif desc_no == 6: return "Die Seherin arbeitet nebenberuflich als Privatdetektiv. Was tut sie diese Nacht?"
	elif desc_no == 7: return "Die Seherin leidet unter Schlafstörungen. Was wird sie diese Nacht unternehmen?"
	elif desc_no == 8: return "Die Seherin ist leidenschaftliche Spannerin. Wen stalkt sie diese Nacht?"
	else: return "Die Seherin kann mal wieder nicht schlafen. Was tut sie diese Nacht?"

def time_to_prosecute():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Es ist Zeit, anzuklagen!"
	elif desc_no == 1: return "Nach einer turbulenten Nacht geht es in Düsterwald heiß her."
	elif desc_no == 2: return "Nach einer solchen Nacht wird in Düsterwald blind beschuldigt."
	elif desc_no == 3: return "Die Dorfbewohner wollen die Übeltäter im Dorf entlarven und beginnen mit den Beschuldigungen."
	elif desc_no == 4: return "Die Dorfbewohner versuchen durch wildes Beschuldigen, die Werwölfe zu enttarnen."
	elif desc_no == 5: return "Jeder versucht, sein eigenes Leben zu schützen und schiebt deshalb die Schuld auf Andere."
	elif desc_no == 6: return "Die Dorfbewohner wollen jemanden für die Verbrechen der Nacht beschuldigen."
	elif desc_no == 7: return "Eine Diskussion entbrandet, wer an den schrecklichen Taten der Nacht schuld sein könnte."
	elif desc_no == 8: return "Eine heiße Diskussion beginnt in Düsterwald. Vage Gerüchte werden auf einmal zu harten Fakten, Werwölfe tarnen sich als normale Büger und harmlose Dorfbewohner werden des brutalen Mordes beschuldigt."
	else: return "Lasset die Beschuldigungsspiele beginnen!"

def time_to_vote():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Es ist Zeit, jemanden hinzurichten!"
	elif desc_no == 1: return "Die Dorfbewohner wollen die Verantwortlichen für die Morde sterben sehen!"
	elif desc_no == 2: return "Die Abstimmung für die Hinrichtung beginnt."
	elif desc_no == 3: return "Wen wollt ihr hinrichten?"
	elif desc_no == 4: return "Wer soll für die grausamen Verbrechen mit einem noch grausameren Tod bezahlen?"
	elif desc_no == 5: return "Wer ist schuldig und muss sterben?"
	elif desc_no == 6: return "Auge um Auge, Zahn um Zahn - und wer muss aufgrund vager Gerüchte einen grauenvollen Tod sterben?"
	elif desc_no == 7: return "Die Demokratie wird entscheiden, wer hingerichtet wird!"
	elif desc_no == 8: return "Das Dorf entscheidet, wer gelyncht wird!"
	else: return "Lasset die Hinrichtungsspiele beginnen!"

def patt_revote():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Pattsituation - bitte nochmals abstimmen!"
	elif desc_no == 1: return "Das Dorf konnte sich nicht entscheiden, wer hingerichtet werden sollte. Deshalb muss die Abstimmung wiederholt werden."
	elif desc_no == 2: return "Die Abstimmung geht unentschieden aus und muss wiederholt werden."
	elif desc_no == 3: return "Die Dorfgemeinschaft kann sich für keinen Schuldigen entscheiden und setzt daher Neuwahlen an."
	elif desc_no == 4: return "Zustände wie in der Türkei: Es wird sooft gewählt, bis den Oberen das Ergebnis gefällt. Es wurden Neuwahlen angesetzt!"
	elif desc_no == 5: return "Es kann nur eine Person hingerichtet werden, irgendjemand sollte seine Meinung ändern!"
	elif desc_no == 6: return "Hier kommt die Demokratie an ihre Grenzen: Die Wahl muss wiederholt werden."
	elif desc_no == 7: return "Eine Koalition ist bei der Hinrichtung nicht möglich. Bitte entscheidet euch für einen Schuldigen."
	elif desc_no == 8: return "Auf dem elekrtischen Stuhl ist nur Platz für eine Person. Bitte nochmals abstimmen!"
	else: return "Wenn ihr zwei halbe Menschen hinrichtet, habt ihr mathematisch auch nur eine Person hingerichtet. Das Problem ist, dass dann beide tot sind. Entscheidet euch!"

def patt_no_kill():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Da sich das Dorf nicht auf einen Schuldigen einigen kann, wird heute niemand gelyncht."
	elif desc_no == 1: return "Die Demokratie ist überfordert un beschließt, niemanden hinzurichten."
	elif desc_no == 2: return "Nach einer intensiven aber ergebnislosen Diskussion kehren alle nach hause zurück."
	elif desc_no == 3: return "Mal wieder viel heiße Luft um Nichts - viel Anschuldigungen aber kein Ergebnis."
	elif desc_no == 4: return "Bei dem versuch, alle Angeklagten zu hängen, reißt das Seil und das Dorf beschließt, heute niemanden hinzurichten."
	elif desc_no == 5: return "Da die Diskussion zu hitzig wird, ohne ein Ergebnis zu zeigen, löst die Polizei die Versammlung auf und schickt alle Beteiligten fort."
	elif desc_no == 6: return "Am Ende des Tages sind alle genervt, da letztlich keiner seine Meinung durchsetzen konnte."
	elif desc_no == 7: return "Dieser Tag geht ohne einen Toten vorbei. Dies sorgt für Unmut unter den Dorfbewohnern, da die Werwölfe auch nächste Nacht nicht ruhen werden."
	elif desc_no == 8: return "Die Dorfbewohner nehmen sich vor: Beim nächsten Mal erzielen wir bei der Abstimmung ein klares Ergebnis, doch momentan will keiner seine Meinung ändern. Vielleicht kann die kommende Nacht gegen ein Patt helfen?"
	else: return "Da sich das Dorf nicht einigen konnte, beschließt es, eine Nacht über die Meinungen zu schlafen. Vielleicht wird man sich ja morgen einig."

def nightfall():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Es wird Nacht in Düsterwald."
	elif desc_no == 1: return "Die Sonne geht langsam unter, es ist Zeit für alle, schlafen zu gehen."
	elif desc_no == 2: return "Düsterwald bereitet sich auf eine turbulente Nacht vor und legt sich schlafen. Manche Individuen stellen sich jedoch einen Wecker..."
	elif desc_no == 3: return "Die Nacht ist nicht weniger gefährlich als der Tag und die Dorfbewohner stellen sich darauf ein, sich vielleicht ein letztes Mal schlafen zu legen..."
	elif desc_no == 4: return "Sowie es langsam dunkel wird in Düsterwald, so legen sich auch alle schlafen."
	elif desc_no == 5: return "Nach einem anstrengenden Tag hoffen viele Dorfbewohner nun auf eine erholsame Nacht. Doch diese Nacht werden nicht alle gut schlafen..."
	elif desc_no == 6: return "Die Straßen werden leer, in der Kneipe wurde schon vor einer halben Stunde das letzte Bier ausgeschenkt und Düsterwald legt sich schlafen."
	elif desc_no == 7: return "Düsterwald legt sich schlafen - in der Hoffnung, in der Morgendämmerung wieder zu erwachen."
	elif desc_no == 8: return "So manch Dorfbewohner hofft nun auf eine ruhige Nacht - andere schlecken sich schon das Maul..."
	else: return "Die Dorfbewohner stoßen auf einen erfolgreichen Tag an und wünschen sich eine gute Nacht."

def wolfshund_options():
	desc_no = random.randrange(0,7)
	if desc_no == 0: return "Wie möchtest du dieses Spiel bestreiten?"
	elif desc_no == 1: return "Welchem Team möchtest du angehören?"
	elif desc_no == 2: return "Welche Gene setzen sich in dir durch?"
	elif desc_no == 3: return "Du kommst jetzt in ein Alter, in dem du dich für eine Seite entscheiden mussst."
	elif desc_no == 4: return "Wie willst du den Rest deines Lebens verbringen?"
	elif desc_no == 5: return "Möchtest du Menschen fressen oder von Menschen gelyncht werden?"
	else: return "Es ist an der Zeit, sich für eine Seite zu entscheiden!"

def wolfshund_choose_werwolf():
	desc_no = random.randrange(0,7)
	if desc_no == 0: return "in einen Werwolf verwandeln"
	elif desc_no == 1: return "zum Werwolf mutieren"
	elif desc_no == 2: return "Das Tier in dir vorkommen lassen"
	elif desc_no == 3: return "Blutlust entwickeln"
	elif desc_no == 4: return "Hunger auf Menschfleisch bekommen"
	elif desc_no == 5: return "dem Dorf den Rücken zuwenden"
	else: return "sich den Werwölfen anschließen"

def wolfshund_choose_dorf():
	desc_no = random.randrange(0,7)
	if desc_no == 0: return "sich dem Dorf anschließen"
	elif desc_no == 1: return "brav im Dorf leben"
	elif desc_no == 2: return "harmloser Schoßhund werden"
	elif desc_no == 3: return "doch lieber Vegetarier werden"
	elif desc_no == 4: return "Wenn du Blut siehst, wird dir schlecht"
	elif desc_no == 5: return "Demokratie der Gewalt vorziehen"
	else: return "Humanität zeigen"
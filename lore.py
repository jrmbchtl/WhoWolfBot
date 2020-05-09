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

def description_terrorwolf():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist der Terrorwolf. Wenn der Terrorwolf stirbt, nimmt er noch einen Spieler seiner Wahl mit in den Tod."
	elif desc_no == 2: return "Du bist der Terrorwolf. Der Terrorwolf ist der Jäger der Werwölfe: Sollte er sterben, kann er noch einen Charakter seiner Wahl mit in den Tod reißen."
	elif desc_no == 3: return "Dein Carakter ist der Terrorwolf, welcher, sollte er zu Tode kommen, in letzter Sekunde noch ein Opfer reißen kann."
	elif desc_no == 4: return "Du bist der Terrorwolf. Dieser ist ähnlich dem Jäger, mit dem Unterschied, dass er für die Werwölfe spielt: Stirbt der Terrorwolf, egal ob bei Tag oder Nacht, so bleibt ihm noch ausreichend Zeit, sich einen Dorfbewohner als Henkersmahlzeit zu schnappen."
	elif desc_no == 5: return "Deine Rolle ist er Terrorwolf, welcher mittels eines Testaments den Tod eines Dorfbewohners einfordert."
	else: return "Du bist der Terrorwolf. Dein Tod hat Konsequenzen. Zumindest für einen weiteren Dorfbewohner: Wenn du stirbst, steht er als letzte Mahlzeit auf deinem Speiseplan."

def description_amor():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist Amor. Amor bestimmt in der ersten Nacht zwei Spieler, die sich unsterblich ineinander verlieben. Diese spielen von nun an zusammen und können gemeinsam gewinnen, auch wenn sie in unterschiedlichen Teams sind."
	elif desc_no == 2: return "Du bist Amor. Mit seinem Bogen und seinen Herzpfeilen sorgt Amor für die Liebe im Düsterwald. Er schießt seine Pfeile auf zwei Dorfbewohner, die sich sofort unsterblich ineinander verlieben und einander bis in den Tod folgen würden. Ihre Liebe ist sogar stärker als ihr Zugehörigkeitsgefühl zu ihrer jeweiligen Partei."
	elif desc_no == 3: return "Dein Charakter ist Amor. Zu Beginn des Spieles bestimmt er zwei Spieler, die sofort in inniger Liebe zueinander entflammen (das kann auch er selbst sein). Stirbt im Laufe des Spiels einer der beiden Liebenden, so auch der andere aus Gram. Achtung: Ist einer der beiden Liebenden ein Werwolf und der andere ein Bürger, so haben sie ein gemeinsames neues Ziel: Überleben sie als einzige so gewinnen sie allein."
	elif desc_no == 4: return "Deine Rolle ist der Amor. Amor erwacht nur einmal in der allerersten Nacht, um zwei Spieler seiner Wahl miteinander zu verkuppeln (eventuell auch sich selbst). Danach schläft er wieder ein. Anschließend lernt sich das frisch verliebte Paar kennen. Die Verliebten haben im Laufe des Spiels die Aufgabe, den Partner zu beschützen, denn wenn einer der beiden stirbt, macht es ihm der Partner trauernd nach; sie dürfen nie gegeneinander stimmen."
	elif desc_no == 5: return "Du bist Amor, welcher dafür sorgt, dass sich zwei Spieler unsterblich ineinander verlieben. Sollte einer von beiden zu Tode kommen, so nimmt sich der andere aus Trauer das Leben. Das Liebespaar kann gemeinsam gewinnen, auch wenn sie von unterschiedlichen Teams sind."
	else: return "Du bist Amor und machst dich in der ersten Nacht auf die Jagd nach einem Liebspaar, welches du verkuppelst. Dieses verliebt sich sofort und will sich nie wieder trennen. Sollte einer von beiden sterben, so bringt der Kummer des Anderen auch ihn ins Grab."

def description_superschurke():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist der Superschurke! Der Superschurke gibt in der ersten Nacht einem Spieler seine herzförmige Bombe. Die Bombe wird am Ende jedes Tages im Uhrzeigersinn weitergegeben. Wenn der Superschurke stirbt, explodiert die Bombe und töten den Spieler, vor dem sie gerade liegt."
	elif desc_no == 2: return "Du bist gewitzt. Du bist brutal. Du bist der Superschurke. Als dieser verdonnerst du in der ersten Nacht mittels einer \"Halt mal kurz\" einen Mitspieler zum Halten einer herzförmigen Bome. Diese wird am Ende jedes Tages im Kreis weitergegeben. Solltest du wider Erwartens zu Tode kommen, so explodiert auch deine herzförmige Bombe und tötet den Spieler, vor dem sie liegt." 
	elif desc_no == 3: return "Dein Charakter ist der Superschurke. Du versteckst in der ersten Nacht eine herzförmige Bombe bei einem Spieler. Dieser findet sie am Ende des Tages und versteckt diese beim nächsten Spieler im Uhrzeigersinn. Wenn du stirbst, detoniert auch die Bombe und sorgt für einen weiteren Toten."
	elif desc_no == 4: return "Bei deiner Rolle handelt es sich um den Superschurken. Dieser kann einem Mitspieler in der ersten nacht eine herzförmige Bombe unterjubeln. Diese wird wie eine heiße Kartoffel am Ende jedes Tages im Uhrzeigersinn weitergeworfen. Wenn dein Herz nicht mehr schlägt, tickt die Bombe ein letztes Mal und tötet den Spieler, der diese momentan hält."
	elif desc_no == 5: return "Dein Charakter ist der Superschurke. Dieser zwingt in der ersten Nacht jemanden dazu, seine herzförmige Bombe zu halten. Dieser ist nicht sonderlich davon begeistert und gibt sie am Ende des Tages im Uhrzeigersinn weiter. Soltest du sterben, so explodiert die Bombe und töten den Halter."
	else: return "Du bist der Superschurke und ein riesiger Fan von Russischem Roulette. Daher bastelst du dir eine herzförmige Bombe, welche du in der ersten Nacht einen Mitspieler gibst. Am Ende jedes Tages wird die Bombe im Uhrzeigersinn weitergegeben. Im Falle deines Ablebens detoniert die Bombe und sorgt dafür, dass der Halter danach aus mehr Einzelteilen besteht als eine Glaswand, die soeben von einem Panzer durchbrochen wurde."

def description_psychopath():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist der Psychopath. Der Psychopath erwacht als letzter Spieler. Wenn in der Nacht niemand gestorben wäre, muss er einen Spieler töten."
	elif desc_no == 2: return "Du bist ein Psychopath, der Menschen sterben sehen will. Sollte in einer Nacht niemand gestorben sein, so erwachst du und musst einen Dorfbewohner töten."
	elif desc_no == 3: return "Du bist ein Psychopath. Wenn du am morgen kein Blut siehst, stimmt dich das traurig. Deshalb erwachst du als letzter Spieler, wenn keiner gestorben ist, und sucht dir dein Opfer."
	elif desc_no == 4: return "Du ist ein Psychopath. Also so ein richtig harter. Eigentich gehörst du in die Klapse, aber bisher ist dir noch niemand auf die Schliche gekommen. Wenn in einer Nacht niemand gestorben ist, so schreckt du kurz vor dem Morgengrauen auf und erdrosselst noch kurz einen Mitspieler."
	elif desc_no == 5: return "Deine Rolle ist der Psychopath. Sollte in einer Nacht niemand gestorben sein, so wirst du geweckt und musst noch jemanden töten."
	else: return "Du bist ein Psychopath. Du hast Lust am morden. Und am Menschen sterben sehen. Deshalb willst du, das jede Nacht jemand stirbt. Un wenn niemand stirbt, stehst du kurz vor Morgendämmerung auf und ermordest noch jemanden."

def description_berserker():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist der Berserker. Der Berserker hat ein Extraleben gegen Werwolfangriffe. Zusätzlich kann er jede Nacht einen Spieler töten, verliert dabei aber auch selbst ein Leben!"
	elif desc_no == 2: return "Du bist ein Berserker, welcher den ersten Werwolfangriff überlebt. Außerdem kann er jede Nacht jemanden töten, allerdings für einen Preis: Für seinen ersten Mord verliert er den Schutz vor den Werölfen, nach seinem zweiten Mord stirbt er vor Erschöpfung."
	elif desc_no == 3: return "Du bist ein Berserker. Du kämpfst in deinem Rausch. Du bist unverwundbar. Naja so fast. Du hast ein Extraleben gegen Werwolfangriffe. Und wenn du willst, kannst du auch jemanden mit deinen Äxten zerstückeln, allerdings verlierst du dann deinen Schutz gegen die Werwölfe."
	elif desc_no == 4: return "Du ist ein Berserker. Ein ziemlich harter und brutaler Zeitgenosse. Du hast ein Extraleben gegen Werwolfangriffe und kannst jede Nacht jemanden töten. Aber Vorsicht: Es gilt Leben für Leben, für jedes Leben, dass du nimmst, verlierst auch du eines!"
	elif desc_no == 5: return "Deine Rolle ist der Berserker. Dieser hat ein Extraleben gegen Werwolfangriffe und schreckt jede Nacht aus seinem Schlaf hoch, mit der Möglichkeit jemanden zu töten. Allerdings verliert der Berserker für jeden Angriff selbst ein Leben."
	else: return "Du bist ein Berserker. Du versuchst, mit Brutalität Gerechtigkeit zu schaffen. Mit deiner Härte, die Werwölfe zu vernichten. Mit deinem Geschick, dem ersten Angriff der Werwölfe zu entkommen. Oder mit deiner Eiseskälte, jemanden zu ermorden. Aber kein Verbrechen, für das nicht bezahlt werden müsste! Beschließt du jemanden zu töten, so verlöierst du deinem Schutz gegen die Werwölfe. Und solltest du keinen Schutz mehr haben, so stirbst du in deinem Wahn, nachdem du dein Opfer erfolgreich erschlagen hast."

def description_terrorist():
	desc_no = random.randrange(1,7)
	if desc_no == 1: return "Du bist der Terrorist. Der Terrorist kann sich zu einem beliebigen Zeitpunkt am Tag in die Luft sprengen und dadurch sich selbst und seine beiden Nachbarn töten. Er kann sich auch noch in die Luft sprengen wenn das Dorf ihn lynchen will, jedoch nicht in seinem Testament."
	elif desc_no == 2: return "Du bist der Terrorist. Dieser kann sich zu jedem beliebigen Zeitpunkt am Tag in die Luft sprengen, solange er lebt und damit sich selbst und seine beiden Nebensitzer töten."
	elif desc_no == 3: return "Deine Rolle ist der Terrorist, welcher einen Sprengstoffgürtel trägt. Diesen kann er jederzeit am Tag zünden, solange er lebt und damit sich selbst und seine direkten Nachbarn zerfetzen."
	elif desc_no == 4: return "Dein Charakter ist der Terrorist, welcher mit einem Sprengstoffgürtel ausgestattet ist. Er kann sich tagsüber dazu entscheiden, den Gürtel zu aktivieren und damit sich selbst und seine zwei Nebensitzer in die Luft zu jagen."
	elif desc_no == 5: return "Du bist der Terrorist, ein selbstloser Selbstmordattetntäter, ausgestattet mit einem explosiven Gürtel, bereit dazu, diesen zu zünden und dich selbst und deine beiden Nachbarn ins Jenseits zu befördern."
	else: return "Deine Kontakte im Nahen Osten haben dir einen Bombengürtel zugespielt und dich zum Terrorist ernannt. Tagsüber kannst du dich in die Luft sprengen, um dich selbst und deine Nebensitzer bei einem Selbtmoranschlag zu töten."

def terrorist_options():
	desc_no = random.randrange(0,8)
	if desc_no == 0: return (0, "Allahu Akbar")
	elif desc_no == 1: return (1, "Sprengstoffgürtel zünden")
	elif desc_no == 2: return (2, "in die Luft sprengen")
	elif desc_no == 3: return (3, "Selbstmord begehen")
	elif desc_no == 4: return (4, "BOOOOOOM")
	elif desc_no == 5: return (5, "ein paar Leben beenden")
	elif desc_no == 6: return (6, "Triple Kill")
	else: return (7, "Let's fetz")

def terrorist_announce(option):
	if option == "0": return "Allahu Akbar!"
	elif option == "1": return "Der Terrorist hat seinen Sprengstoffgürtel gezündet."
	elif option == "2": return "Der Terrorist hat sich in die Luft gesprengt."
	elif option == "3": return "Der Terrorist ist in die Luft geflogen."
	elif option == "4": return "BOOOOOOM!"
	elif option == "5": return "Der Terrorist hat ein paar Leben beendet!"
	elif option == "6": return "Triple Kill!"
	else: return "Let's fetz!"

def berserker_question(extra_life):
	base_text = ""
	if extra_life: base_text = "Du hast 2 Leben. "
	else: base_text = "Du hast nur noch ein Leben."
	desc_no = random.randrange(0,10)
	if desc_no == 0: return (0, base_text + "Wen möchtest du ermorden?")
	elif desc_no == 1: return (1, base_text + "Wen willst du mit deinen Äxten besuchen?")
	elif desc_no == 2: return (2, base_text + "Wer soll morgens mit einer Axt im Kopf aufgefunden werden")
	elif desc_no == 3: return (3, base_text + "Wer könnte ein Werwolf sein und muss dafür sterben?")
	elif desc_no == 4: return (4, base_text + "Du erhälst die Möglichkeit, jemanden zu töten. Wer wird es sein?")
	elif desc_no == 5: return (5, base_text + "Wer wird heute Nacht dem Berserker zum Opfer fallen?")
	elif desc_no == 6: return (6, base_text + "Es ist Zeit für dich, jemanden zu töten!")
	elif desc_no == 7: return (7, base_text + "Wer dient als Zielscheibe für dein nächtliches Axtwerfen?")
	elif desc_no == 8: return (8, base_text + "Wen greifst du diese Nacht im Rausch an?")
	else: return (9, base_text + "Wen willst du wie ein wildes Tier anfallen?")

def berserker_response(option, name):
	if option == "0": return "Du hast " + name + " ermordet."
	elif option == "1": return "Der Berserker hat " + name + " mit seinen Äxten besucht."
	elif option == "2": return "Du hast " + name + " eine Axt in den Kopf geschlagen."
	elif option == "3": return "Du hast " + name + " sterben lassen."
	elif option == "4": return "Der Berserker hat vermutet, dass " + name + " ein Werwolf ist, kurzen Prozess gemacht und ihn schnell enthauptet."
	elif option == "5": return "Der Berserker hat " + name + " überfallen."
	elif option == "6": return "Der Berserker hat " + name + " getötet."
	elif option == "7": return "Der Berserker hat " + name + " als Zielscheibe genutzt."
	elif option == "8": return "Du hast " + name + " in deinem Rausch angegriffen."
	else: return "Der Berserker hat " + name + " wie ein wildes Tier angefallen."

def psycho_intro():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Es ist bisher niemand gestorben. Das wird sich jetzt ändern..."
	elif desc_no == 1: return "Der Psychopath erwacht und verspürt Lust auf einen Mord."
	elif desc_no == 2: return "Der Psychopath hat das Verlangen, jemanden zu töten."
	elif desc_no == 3: return "Du schaust dich in der Morgendämmerung im Dorf um un siehst: Bisher ist niemand gestorben. Das kannst du nicht so lassen."
	elif desc_no == 4: return "Der Psychopath erwacht im Angstschweiß: Bisher ist diese Nacht noch niemand gestorben..."
	elif desc_no == 5: return "Wähle dein Opfer, Psychopath!"
	elif desc_no == 6: return "Es ist Zeit für dich, jemanden zu töten!"
	elif desc_no == 7: return "Du denkst dir: Man kann ja so eine Nacht nicht ohne einen Toten beenden..."
	elif desc_no == 8: return "In den frühen Morgenstunden machst du dich auf und suchst dein Opfer..."
	else: return "Eine Nacht ohne Blut ist doch keine Nacht..."

def inlineKey_psychopath_options(name):
	desc_no = random.randrange(0,10)
	if desc_no == 0: return (0, name + " strangulieren")
	elif desc_no == 1: return (1, name + " ermorden")
	elif desc_no == 2: return (2, name + " kaltblütig zerstückeln")
	elif desc_no == 3: return (3, name + " überfahren")
	elif desc_no == 4: return (4, name + " von einer Klippe stoßen")
	elif desc_no == 5: return (5, name + " einmauern")
	elif desc_no == 6: return (6, name + " ein Messer in die Brust rammen")
	elif desc_no == 7: return (7, name + " in eine Sprengfalle locken")
	elif desc_no == 8: return (8, name + " mit einem Löffel erschlagen")
	else: return (9, name + " in den Backofen stecken")

def psyhopath_response_options(option, name):
	if option == "0": return "Du hast " + name + " stranguliert."
	elif option == "1": return "Der Psychopath hat " + name + " ermordet."
	elif option == "2": return "Du hast " + name + " kaltblütig zerstückelt."
	elif option == "3": return "Der Psychopath hat " + name + " überfahren."
	elif option == "4": return "Der Psychopath hat " + name + " von einer Klippe gestoßen."
	elif option == "5": return "Der Psychopath hat " + name + " eingemauert."
	elif option == "6": return "Der Psychopath hat " + name + " ein Messer in die Brust gerammt."
	elif option == "7": return "Du hast " + name + " in eine Sprengfalle gelockt."
	elif option == "8": return "Du hast " + name + " mit einem Löffel erschlagen."
	else: return "Der Psychopath hat " + name + " in den Backofen gesteckt."

def superschurke_options():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return (0, "Wem willst du die herzförmige Bombe geben?")
	elif desc_no == 1: return (1, "Wem möchtest du mit einer herzförmigen Bombe deine Liebe vorspielen")
	elif desc_no == 2: return (2, "Wem willst du mit der herzförmigen Bombe zu einem \"Halt mal kurz\" verdonnern?")
	elif desc_no == 3: return (3, "Wer muss die herzförmige Bombe zu Beginn halten?")
	elif desc_no == 4: return (4, "Wer darf als erstes bei deiner Version von russischem Roulette die Bombe halten?")
	elif desc_no == 5: return (5, "Wer bekommt die heiße Kartoffel?")
	elif desc_no == 6: return (6, "Wer soll der erste stolze Besitzer der herzförmigen Bombe werden?")
	elif desc_no == 7: return (7, "Wem willst du die herzförmige Bombe unterjubeln?")
	elif desc_no == 8: return (8, "Wessen Kissen tauschst du diese Nacht gegen die herzförmige Bombe aus?")
	else: return (9, "Wer bekommt die Ehre, Halter der herzförmigen Bombe zu werden?")

def superschurke_response(option, name):
	if option == "0": return "Du hast " + name + " die Bombe gegeben."
	elif option == "1": return "Der Superschurke hat " + name + " seine Liebe mit einer herzförmigen Bombe vorgespielt."
	elif option == "2": return "Du hast " + name + " mit einem \"Halt mal kurz\" erwischt."
	elif option == "3": return "Der Superschurke hat " + name + " die Bombe gegeben."
	elif option == "4": return "Der Superschurke hat " + name + " als ersten Mitspieler von russischem Roulette ausgesucht."
	elif option == "5": return "Der Superschurke hat " + name + " die heiße Kartoffel gegeben."
	elif option == "6": return "Der Superschurke hat " + name + " zum stolzen Besitzer der herzförmigen Bombe ernannt."
	elif option == "7": return "Du hast " + name + " die Bombe untergejubelt."
	elif option == "8": return "Du hast " + name + "s Kissen mit der herzförmigen Bombe ausgetauscht."
	else: return "Der Superschurke hat " + name + " die Bombe in die Hand gedrückt."

def amor_question():
	desc_no = random.randrange(0,8)
	if desc_no == 0: return "Wer soll sich dieses Spiel verlieben?"
	elif desc_no == 1: return "Wen willst du mit deinen Liebespfeilen treffen?"
	elif desc_no == 2: return "Wer gibt ein schönes Liebespaar ab?"
	elif desc_no == 3: return "Wen willst du verkuppeln?"
	elif desc_no == 4: return "Wer soll sich heute Nacht verlieben?"
	elif desc_no == 5: return "Wer wird heute Nacht seinen Traumpartner finden?"
	elif desc_no == 6: return "Wer wird sich gleich unsterblich verlieben?"
	else: return "Wer findet die Liebe des Lebens?"

def get_loved_one_killed():
	desc_no = random.randrange(0,8)
	if desc_no == 0: return " stirbt aus Liebskummer\\."
	elif desc_no == 1: return " will nicht ohne seinen Partner weiterleben\\."
	elif desc_no == 2: return " kann alleine nicht überleben\\."
	elif desc_no == 3: return " hängt sich aus Trauer\\."
	elif desc_no == 4: return " wird todtraurig und stirbt\\."
	elif desc_no == 5: return " überlebt den Herzschmerz nicht\\."
	elif desc_no == 6: return " will nicht ohne Liebe leben\\."
	else: return " hält es alleine nicht mehr aus und begeht Suizid\\."

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

def terrorist_death_message():
	desc_no = random.randrange(1,11)
	if desc_no == 1: return " wurden von dem Terrorist erwischt\\."
	elif desc_no == 2: return " bestehen aus mehr Einzelteilen als eine Lego Sternsterörer\\."
	elif desc_no == 3: return " sind im ganzen Dorf verteilt\\."
	elif desc_no == 4: return " garnieren den Dorfplatz mit einer Ketchupähnlichen Substanz\\."
	elif desc_no == 5: return " hat es im wahrsten Sinne des Wortes verrissen\\."
	elif desc_no == 6: return " wurden pulverisiert\\."
	elif desc_no == 7: return " waren ungesund nahe an einer größeren Menge explodierendem Schwarzpulver\\."
	elif desc_no == 8: return " wurden von einer Sprengstoffgürtel getroffen\\."
	elif desc_no == 9: return " überlebten die Explosion eines Sprengstoffgürtels nicht\\."
	else: return " können den Diskussionen des Dorfes nur noch in Stücken folgen\\."

def bomb_death_message():
	desc_no = random.randrange(1,11)
	if desc_no == 1: return " wurde von der Bombe erwischt\\."
	elif desc_no == 2: return " besteht aus mehr Einzelteilen als eine Lego Sternsterörer\\."
	elif desc_no == 3: return " verteilt sich im ganzen Dorf\\."
	elif desc_no == 4: return " garniert den Dorfplatz mit einer Ketchupähnlichen Substanz\\."
	elif desc_no == 5: return " hat es im wahrsten Sinne des Wortes verrissen\\."
	elif desc_no == 6: return " wurde pulverisiert\\."
	elif desc_no == 7: return " war ungesund nahe an einer größeren Menge explodierendem Schwarzpulver\\."
	elif desc_no == 8: return " wurde von einer Nagelbombe getroffen\\."
	elif desc_no == 9: return " überlebte die Explosion einer schnutzigen Bombe in seinem Rucksack nicht\\."
	else: return " kann den Diskussionen des Dorfes nur noch in Stücken folgen\\."

def death_message(gender):
	desc_no = random.randrange(1,16)
	if desc_no == 1: return " ist diese Nacht leider gestorben\\."
	elif desc_no == 2: return " erblickt das Licht des neuen Tages nicht mehr\\."
	elif desc_no == 3: return " wurde massakriert aufgefunden\\."
	elif desc_no == 4: return " existiert nur noch in Stücken\\."
	elif desc_no == 5: return " hat die letzten Stunden nicht überlebt\\."
	elif desc_no == 6: return " ist nicht mehr aufzufinden\\."
	elif desc_no == 7 and gender == "female" : return " war eine gute Kameradin\\."
	elif desc_no == 7: return " war ein guter Kamerad\\."
	elif desc_no == 8 and gender == "female" : return " hat ihren letzten Kampf verloren\\."
	elif desc_no == 8: return " hat seinen letzten Kampf verloren\\."
	elif desc_no == 9: return " hat den Löffel abgegeben\\."
	elif desc_no == 10: return " besucht nun die ewigen Jagdgründe\\."
	elif desc_no == 11: return " hat leider ins Gras gebissen\\."
	elif desc_no == 12: return " wird nie wieder an den Freuden des Dorfes teilhaben\\."
	elif desc_no == 13: return " ist von uns gegangen\\."
	elif desc_no == 14: return " ist über die Wupper gegangen\\."
	else:  return " hat das Zeitliche gesegnet\\."

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
	if option == "0": return " wurde gehängt\\."
	elif option == "1": return " wird auf dem Scheiterhaufen verbrannt\\!"
	elif option == "2": return " bekommt den Schwedentrunk verabreicht\\."
	elif option == "3": return " wurde gevierteilt\\."
	elif option == "4": return " hat sich für das Gemeinwohl opfern lassen\\."
	elif option == "5": return " wurde ertränkt\\!"
	elif option == "6": return " wird von einem Felsen gestürzt\\."
	elif option == "7": return " ist unter der Guillotine gelandet\\!"
	elif option == "8": return " wurde lebendig begraben\\."
	else: return " hat die Steinigung nicht überlebt\\."

def inlineKey_terrorwolf_options():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return (0," reißen")
	elif desc_no == 1: return (1," als Henkersmahlzeit verspeißen")
	elif desc_no == 2: return (2," mit in den Tod reißen")
	elif desc_no == 3: return (3," noch kurz verputzen")
	elif desc_no == 4: return (4," im Vorbeilaufen die Zähne in den Hals rammen")
	elif desc_no == 5: return (5," mit letzter Kraft zerbeißen")
	elif desc_no == 6: return (6," noch kurz in der Luft zerfetzen")
	elif desc_no == 7: return (7," bei einem Attentäter in Auftrag geben")
	elif desc_no == 8: return (8," tödliche Schürfwunden verpassen.")
	else: return (9," aus Mitleid noch kurz aufessen")

def terrorwolf_kill(option, gender):
	if option == "0": return " wurde vom Terrorwolf gerissen\\."
	elif option == "1": return " wurde als Henkersmahlzeit verspeißt\\!"
	elif option == "2": return " wurde mit in den Tod gerissen\\."
	elif option == "3": return " wurde noch kurz verputzt\\."
	elif option == "4": return " hat sich im Vorbeilaufen die Zähne in den Hals rammen lassen\\."
	elif option == "5": return " wurde mit der letzen Kraft des Terrorwolfes zerbissen\\."
	elif option == "6": return " wurde in der Luft zerfetzt\\."
	elif option == "7": return " wurde bei einem Attentäter in Auftrag gegeben und konnte nicht entkommen\\."
	elif option == "8" and gender == "female": return " kann ohne ihren Kopf nicht weiterleben\\!"
	elif option == "8": return " kann ohne seinen Kopf nicht weiterleben\\!"
	else: return " wurde noch kurz aus Mitleid aufgegessen\\."

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
	if option == "0": return " wurde vom Jäger erschossen\\."
	elif option == "1": return " wurde mit einer Nagelpistole an die Wand geheftet\\!"
	elif option == "2": return " hat nun sehr viele Löcher in Kopf und Brust\\."
	elif option == "3": return " wurde umgelegt\\."
	elif option == "4": return " hat sich wegpusten lassen\\."
	elif option == "5": return " wurde in der Notwehr des Jägers erschossen\\!"
	elif option == "6": return " wurde niedergestreckt\\."
	elif option == "7": return " endete als letzte Jagdtrophäe des Jägers\\!"
	elif option == "8": return " wurde vom Jäger mit in den Tod gerissen\\."
	else: return " hat einen Gnadenschuss erhalten\\."

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
	if desc_no == 0: return (0,"Retten")
	elif desc_no == 1: return (1,"Heilen")
	elif desc_no == 2: return (2,"Einen Lebenstrank verabreichen")
	elif desc_no == 3: return (3,"Erfolgreich die Verletzungen versorgen")
	elif desc_no == 4: return (4,"Wiederbeleben")
	else: return (5,"Wieder zusammennähen")

def hexe_let_die():
	desc_no = random.randrange(0,8)
	if desc_no == 0: return (0,"Sterben lassen")
	elif desc_no == 1: return (1,"Nicht beachten")
	elif desc_no == 2: return (2,"Dem Schicksal überlassen")
	elif desc_no == 3: return (3,"Ausversehen zu spät kommen")
	elif desc_no == 4: return (4,"Lieber schlafen")
	elif desc_no == 5: return (5,"Umdrehen und weiterschlafen")
	elif desc_no == 6: return (6,"Lebenstrank nicht für sojemanden verschwenden")
	else: return (7,"Eigensicherung vorziehen")

def hexe_did_save(option, name):
	if option == "0": return "Du hast " + name + " gerettet."
	elif option == "1": return "Die Hexe hat " + name + " geheilt."
	elif option == "2": return "Die Hexe hat " + name + " einen Lebenstrank verabreicht."
	elif option == "3": return "Du hast " + name + "s Verletzungen erfolgreich versorgt."
	elif option == "4": return "Die Hexe hat " + name + " wiederbelebt."
	else: return "Die Hexe hat " + name + " wieder zusammengenäht."

def hexe_did_let_die(option, name):
	if option == "0": return "Du hast " + name + " sterben gelassen."
	elif option == "1": return "Die Hexe hat " + name + " nicht beachtet."
	elif option == "2": return "Die Hexe hat " + name + " dem Schicksal überlassen."
	elif option == "3": return "Du bist für " + name + " ausversehen zu spät gekommen."
	elif option == "4": return "Die Hexe hat lieber geschlafen, als " + name + " zu helfen."
	elif option == "5": return "Die Hexe hat sich einfach umgedreht und weitergeschlafen, als sie von " + name + "s Unfall hörte."
	elif option == "6": return "Die Hexe wollte ihren Lebenstrank nicht für jemanden wie " + name + " verschwenden."
	else: return "Die Hexe hat Eigensicherung vorgezogen statt " + name + " zur Hilfe zu eilen."

def hexe_kill():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return (0," vergiften")
	elif desc_no == 1: return (1," den Todestrank einflößen")
	elif desc_no == 2: return (2," eine ungesunde Substanz injezieren")
	elif desc_no == 3: return (3," ausversehen eine Überdosis Morphium verabreichen")
	elif desc_no == 4: return (4," mit radioaktivem Gemüse versorgen")
	elif desc_no == 5: return (5,"s innere Organe verätzen")
	elif desc_no == 6: return (6," ausversehen Gift in das Getränk mischen")
	elif desc_no == 7: return (7," ein Essen mit Fliegenpilzen zubereiten")
	elif desc_no == 8: return (8," einen Kugelfisch falsch zubereiten")
	else: return (9," Quecksilber in die Milch mischen")

def hexe_did_kill(option, name):
	if option == "0": return "Du hast " + name + " vergiftet."
	elif option == "1": return "Die Hexe hat " + name + " den Todestrank eingeflöst."
	elif option == "2": return "Die Hexe hat " + name + " eine ungesunde Substanz injeziert."
	elif option == "3": return "Du hast " + name + " eine Überdosis Morphium verabreicht."
	elif option == "4": return "Die Hexe hat  " + name + " mit radioaktivem Gemüse versorgt."
	elif option == "5": return "Du hast " + name + "s innere Organe verätzt."
	elif option == "6": return "Die Hexe hat ausversehen " + name + " Gift ins Getränk gemischt."
	elif option == "7": return "Die Hexe hat " + name + " ein Essen mit Fliegenpilzen zubereitet."
	elif option == "8": return "Du hast einen kleinen Fehler gemacht, als du den Kugelfisch für " + name + " zubereitet hast."
	else: return "Die Hexe hat " + name + " Quecksilber in die Milch gemischt."

def all_dead():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Es sind alle tot\\."
	elif desc_no == 1: return "Das Dorf ist so lebendig wie Tschernobyl\\."
	elif desc_no == 2: return "In Düsterwald könnte jetzt ein Vulkan ausbrechen und niemand würde sterben\\."
	elif desc_no == 3: return "Düsterwald hat seine Letzte Ruhe gefunden\\."
	elif desc_no == 4: return "Jetzt leben nur noch Tiere in Düsterwald\\."
	elif desc_no == 5: return "Die Natur wird sich das kleine Örtchen ab jetzt Stück für Stück zurückholen\\."
	elif desc_no == 6: return "Die Zivilisation in Düsterwald ist ausgelöscht\\."
	elif desc_no == 7: return "Das Werwolfproblem ist beseitigt\\. Das Menschenproblem aber auch\\."
	elif desc_no == 8: return "Düsterwald hat jetzt " + str(json.loads(requests.get("http://api.open-notify.org/astros.json").text)["number"]) + " Einwohner weniger als das Weltall\\."
	else: return "Das Kapitel 'Düsterwald' ist jetzt endgültig abgeschlossen\\."

def werwoelfe_win():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Die Werwölfe gewinnen\\."
	elif desc_no == 1: return "Es war ein langer Kampf, aber die Werwölfe haben sich durchgesetzt\\."
	elif desc_no == 2: return "Es leben nur noch Werwölfe in Düsterwald\\!"
	elif desc_no == 3: return "Es gibt keine Dorfbewohner mehr, die von den Werwölfen verspeißt werden können\\."
	elif desc_no == 4: return "Es wird wieder friedlich in Düsterwald, da hier jetzt nur noch Werwölfe leben\\."
	elif desc_no == 5: return "Die Werwölfe haben gesiegt\\."
	elif desc_no == 6: return "Die Werwölfe haben ihre Dominanz bewiesen\\."
	elif desc_no == 7: return "Die Werwölfe sind in Düsterwald anscheinend die stärkere Rasse\\."
	elif desc_no == 8: return "Mit dem Tod des letzten Dorfbewohners haben die Werwölfe jetzt ihre Ruhe\\."
	else: return "Die Werwölfe veranstalten zur Feier des Tages einen Fest und verspeißen genussvoll den letzten Dorfbewohner\\."

def dorf_win():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Das Dorf gewinnt\\."
	elif desc_no == 1: return "Es war ein langer Kampf, aber die Dorfbewohner haben sich durchgesetzt\\."
	elif desc_no == 2: return "Es leben keine Werwölfe mehr in Düsterwald\\!"
	elif desc_no == 3: return "Es gibt keine Werwölfe mehr, die Dorfbewohner verspeißen wollen\\."
	elif desc_no == 4: return "Es wird wieder friedlich in Düsterwald, da hier nur noch Dorfbewohner leben\\."
	elif desc_no == 5: return "Die Dorfbewohner haben gesiegt\\."
	elif desc_no == 6: return "Die Dorfbewohner haben ihre Dominanz bewiesen\\."
	elif desc_no == 7: return "Die Werwölfe sind in Düsterwald anscheinend die unterlegene Rasse\\."
	elif desc_no == 8: return "Mit dem Tod des letzten Werwolfes haben die Dorfbewohner jetzt ihre Ruhe\\."
	else: return "Die Dorfbewohner veranstalten zur Feier des Tages einen Fest und stopfen den letzten Werwolf aus\\."

def love_win():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Das Liebespaar gewinnt\\."
	elif desc_no == 1: return "Die Liebe hat in Düsterwald gesiegt\\."
	elif desc_no == 2: return "Die Liebe bringt nun Licht nach Düsterwald\\!"
	elif desc_no == 3: return "Es lebt nur noch das Liebespaar\\."
	elif desc_no == 4: return "Es wird wieder friedlich in Düsterwald, da das Liebespaar als letztes überlebt.\\."
	elif desc_no == 5: return "Die Liebe bringt nun Frieden nach Düsterwald\\."
	elif desc_no == 6: return "Die Liebe hat ihre Überlegenheit demonstriert\\."
	elif desc_no == 7: return "Liebe überwindet alles\\."
	elif desc_no == 8: return "Die Liebe hat sich durchgesetzt\\."
	else: return "Das Liebespaar genießt die Ruhe zu zweit\\."

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

def terrorwolf_reveal():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return " war der Terrorwolf!"
	elif desc_no == 1: return " will noch jemanden in seinem Testament zerfleischen lassen."
	elif desc_no == 2: return " reißt sein Maul auf: Ihm bleibt noch genügend Zeit, jemanden zu fressen"
	elif desc_no == 3: return " beißt einen Dorfbewohner!"
	elif desc_no == 4: return " will seinen Freunden mit seinem Tod helfen und sucht sich eine Henkersmahlzeit."
	elif desc_no == 5: return " kriegt vor seinem Tod nochmal Hunger."
	elif desc_no == 6: return " will im Sterben noch jemanden versnacken!"
	elif desc_no == 7: return " will nicht alleine sterben und fletscht die Zähne."
	elif desc_no == 8: return " genießt es, jemanden zu sehen - und zerfetzt ihn!"
	else: return " fordert sein Recht ein - vor dem Tod noch ein letztes Mal Beute fangen."

def terrorwolf_choose_target():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return "Wen möchtest du mit ins Grab nehmen?"
	elif desc_no == 1: return "Wen möchtest du zerfleischen?"
	elif desc_no == 2: return "Wen willst du versnacken?"
	elif desc_no == 3: return "Wen willst du in Notwehr zerfetzen?"
	elif desc_no == 4: return "Wen willst du 'ausversehen' mit deinen Zähnen füllen?"
	elif desc_no == 5: return "Wem möchtest du wortwörtlich den Kopf abreißen?"
	elif desc_no == 6: return "Wem möchtest du dazu verhelfen, an inneren Blutungen zu erliegen?"
	elif desc_no == 7: return "Wen willst du als letzten Akt zerreißen?"
	elif desc_no == 8: return "Wem gönnst du es nicht, ohne dich weiterzuleben?"
	else: return "Wer soll durch deine Krallen seine ewige Ruhe finden?"

def jaeger_reveal():
	desc_no = random.randrange(0,10)
	if desc_no == 0: return " war der Jäger!"
	elif desc_no == 1: return " schießt rücksichtslos, um nicht alleine sterben zu müssen!"
	elif desc_no == 2: return " trägt eine geladene Waffe bei sich!"
	elif desc_no == 3: return " zückt eine Schrotflinte!"
	elif desc_no == 4: return " versucht mit Waffengewalt, kurz vor seinem Tod noch für Gerechtigkeit zu sorgen!"
	elif desc_no == 5: return " hat einen Jagdschein!"
	elif desc_no == 6: return " hat eine Jagdlizenz. Jetzt auch für Menschen!"
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
	elif desc_no == 1: return "Die Demokratie ist überfordert und beschließt, niemanden hinzurichten."
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
	if desc_no == 0: return (0,"in einen Werwolf verwandeln")
	elif desc_no == 1: return (1,"zum Werwolf mutieren")
	elif desc_no == 2: return (2,"das Tier in dir vorkommen lassen")
	elif desc_no == 3: return (3,"Blutlust entwickeln")
	elif desc_no == 4: return (4,"Hunger auf Menschfleisch bekommen")
	elif desc_no == 5: return (5,"dem Dorf den Rücken zuwenden")
	else: return (6,"sich den Werwölfen anschließen")

def wolfshund_did_chose_werwolf(option):
	if option == "0": return "Du hast dich in einen Werwolf verwandelt."
	elif option == "1": return "Du bist zu einem Werwolf mutiert."
	elif option == "2": return "Du hast das Tier in dir durchkommen lassen."
	elif option == "3": return "Du hast Blutlust enwickelt."
	elif option == "4": return "Du hast Hunger auf Menschfleisch bekommen."
	elif option == "5": return "Du hast dem Dorf den Rücken zugewendet."
	else: return "Du hast dich den Werwölfen angeschlossen."

def wolfshund_choose_dorf():
	desc_no = random.randrange(0,7)
	if desc_no == 0: return (0,"sich dem Dorf anschließen")
	elif desc_no == 1: return (1,"brav im Dorf leben")
	elif desc_no == 2: return (2,"harmloser Schoßhund werden")
	elif desc_no == 3: return (3,"doch lieber Vegetarier werden")
	elif desc_no == 4: return (4,"Wenn du Blut siehst, wird dir schlecht")
	elif desc_no == 5: return (5,"Demokratie der Gewalt vorziehen")
	else: return (6,"Humanität zeigen")

def wolfshund_did_chose_dorf(option):
	if option == "0": return "Du hast dich dem Dorf angeschlossen."
	elif option == "1": return "Du lebst von nun an brav im Dorf."
	elif option == "2": return "Du bist zu einem harmlosen Schoßhund geworden."
	elif option == "3": return "Du hast beschlossen, doch lieber Vegetarier zu werden."
	elif option == "4": return "Du hast Hämatophobie."
	elif option == "5": return "Du ziehst die Demokratie der Gewalt vor."
	else: return "Du zeigst Humanität."
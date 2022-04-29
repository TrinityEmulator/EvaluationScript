# Evaluation Data and Scripts
![status](https://github.com/TrinityEmulator/EvaluationScript/actions/workflows/python-app.yml/badge.svg)

Here contains the evaluation scripts for generating our major figures in Trinity's paper. 

### 1. Requirements
To run the scripts, you'll
need first to install the `Python 3` environment. Also, we have some additional dependencies. To install them,
type `pip3 install -r requirements.txt` at the root directory of the repo. 

### 2. Script Usages
To run a script named `xxx.py`, simpy type `python3 xxx.py` in your terminal. The scripts' functions are detailed as
follows.

* `DrawBenchmarkFigure.py`

  This script draws `Figure 4` and `Figure 5`. drawn Figures are placed in `Game/fig`.

* `DrawAppFigure.py`
  
  This script draws `Figure 6`~`Figure 10`. drawn Figures are placed in `Benchmark/fig`.

* `DrawDataTransferBench.py`
 
  This script draws `Figure 11`~`Figure 14`. drawn Figures are placed in `DataTransferBench/fig`.

### 3. Data Format

#### Benchmark
The raw benchmark data live in `Benchmark/Benchmark.xlsx`. It contains four data sheets, titled `{3DMark, GFXBench}_{External, Internal}`. Here `{3DMark, GFXBench}` refers to the two benchmark apps we test, and `{External, Internal}` refers to the tests on high-end and middle-end PCs, respectively.
Specific data format is documented is the first row and colum of each data sheet.

#### 3D App
3D app test results are included in `Game`. Here you'll find five folders named after the games we test, each of which contain the data for different emulators. 

Within the emulators' folders, you can find the raw data of FPS recorded during evaluation. In particular, there are two types of FPS raw data files with `hml` and `csv` suffixes, respectively, as we use different FPS measurement tools for DAOW and Bluestacks as they lack system-level supports for FPS capturing. 

However, you'll find that `hml` files are essentially the same as a `csv` one. You can find FPS data under the colum `Framerate` for `hml` files. For `csv` files, the second colum is the FPS data.

#### Data Transfer
This part of data are those of `Figure 11`~`Figure 14` (see Section 4.4 of our paper for detailed explanations), and are located in `DataTransferBench`. Specific descriptions of different folders are listed here.
| Folder | Description |
| ---  | --- |
| `teleporting` | Benchmark data of data teleporting |
| `goldfish-pipe` | Benchmark data of goldfish-pipe |
| `async_polling` | Benchmark data of teleporting with a fixed async + host polling strategy |
| `async_polling_aggregation` | Benchmark data of teleporting with a fixed async + host polling + data aggregation strategy |
| `sync_polling` | Benchmark data of teleporting with a fixed sync + host polling strategy |
| `sync_polling_aggregation` | Benchmark data of teleporting with a fixed sync + host polling + data aggregation strategy |
| `sync_vm-exit` | Benchmark data of teleporting with a fixed sync + VM_EXIT strategy |
| `sync_vm-exit_aggregation` | Benchmark data of teleporting with a fixed sync + VM_EXIT + data aggregation strategy |

Within each of the folder, there are a number of subfolders, whose name follows the convention of `{data_chunk_size in byte}_{number of threads}_0`. Each of the subfolder contains a `throughput.txt` file that hosts the raw throughput data we have measured in evaluation.


### 4. Top-100 3D Apps

Below is the list of the top-100 3D apps from Google Play.

| ID | App Name | Package Name |
| ---- | ---- | ---- |
| 1 | Alien Zone Plus | com.alienzoneplus |
| 2 | Horizon Chase | com.aquiris.horizonchase |
| 3 | Dawn break Origin | com.auer.dawnbreak.trial.single.player.free |
| 4 | Demolition Derby 2 | com.BeerMoneyGames.Demolition2 |
| 5 | Grimvalor | com.direlight.grimvalor |
| 6 | Star Combat Online | com.drspritz.starcombat |
| 7 | Broken Dawn Plus HD | com.dw.zy.gp.hd |
| 8 | Space Commander: War andr Trade | com.HomeNetGames.SpaceCommander |
| 9 | Rivals at War: 2084 | com.hotheadgames.google.free.rawspace |
| 10 | Temple Run | com.imangi.templerun |
| 11 | Temple Run 2 | com.imangi.templerun2 |
| 12 | Fast Racing 3D | com.julian.fastracing |
| 13 | GT CL Drag Racing CSR Car Game | com.kingkodestudio.z2h |
| 14 | Traffic Racer | com.skgames.trafficracer |
| 15 | World of Tanks Blitz | net.wargaming.wot.blitz |
| 16 | Extreme Car Driving Simulator | com.aim.racing |
| 17 | Hashiriya Drifter Car Racing | com.car.games.drifter.driving.simulator |
| 18 | CarX Highway Racing | com.CarXTech.highWay |
| 19 | Nitro Nation: Car Racing Game | com.creativemobile.nno |
| 20 | Stay Alive - Zombie Survival | com.dokoli.sa |
| 21 | Dragon Storm Fantasy | com.dsfgland.goat |
| 22 | Zombie Frontier 3: Sniper FPS | com.feelingtouch.zf3d |
| 23 | Zombie Frontier 4: Shooting 3D | com.feelingtouch.zfsniper |
| 24 | Dream League Soccer 2022 | com.firsttouchgames.dls7 |
| 25 | Score! Hero | com.firsttouchgames.hero2 |
| 26 | Marvel Strike Force: Squad RPG | com.foxnextgames.m3 |
| 27 | Sniper 3D Gun Shooting Games | com.fungames.sniper3d |
| 28 | Cover Fire: Offline Shooting | com.generagames.resistance |
| 29 | Western Survival: Cowboy Game | com.heliogames.westland |
| 30 | Assoluto Racing | com.infinityvector.assolutoracing |
| 31 | Last Hope Sniper - Zombie War | com.JESoftware.LastHopeSniperWar |
| 32 | Subway Surfers | com.kiloo.subwaysurf |
| 33 | Punishing: Gray Raven | com.kurogame.gplay.punishing.grayraven.en |
| 34 | Shadowgun Legends - Online FPS | com.madfingergames.legends |
| 35 | RACE: Rocket Arena Car Extreme | com.smokoko.race |
| 36 | Top Speed: Drag Fast Racing | com.tbegames.and.top_speed_racing |
| 37 | Galaxy Reavers 2 | com.tbreavers.galaxy |
| 38 | Endless Nightmare 2: Hospital | endless.nightmare.weird.hospital.horror.scary.free.android |
| 39 | Top Eleven Be a Soccer Manager | eu.nordeus.topeleven.android |
| 40 | Zombie Hunter: offline Games | zombie.survival.dead.shooting |
| 41 | Prey Day: Survive the Zombie Apocalypse | zombie.survival.online.craft |
| 42 | Payback 2 The Battle Sandbox | net.apex_designs.payback2 |
| 43 | Unkilled zombie Games FPS | com.madfingergames.unkilled |
| 44 | Real Car Parking Master: Multiplayer Car Game | com.SpektraGames.ParkingMasterMultiplayerCarGame |
| 45 | AWP Mode: Online Sniper Action | com.alphainteractive.sniperawpshooter |
| 46 | Bullet Force | com.blayzegames.iosfps |
| 47 | CarX Rally | com.carxtech.rally |
| 48 | Critical Strike CS: Counter Terrorist Online FPS | com.critical.strike2 |
| 49 | Garena Free Fire MAX | com.dts.freefiremax |
| 50 | Garena Free Fire | com.dts.freefireth |
| 51 | Real Racing  3 | com.ea.games.r3_na |
| 52 | Code of War | com.extremedevelopers.codeofwar |
| 53 | WWR: War Robots Games | com.extremedevelopers.wwr |
| 54 | Era Origin | com.eyougame.eo |
| 55 | War Machines: Tank Army Game | com.fungames.battletanksbeta |
| 56 | Infinity Ops: Cyberpunk FPS | com.gamedevltd.destinywarfare |
| 57 | Modern Strike Online: PvP FPS | com.gamedevltd.modernstrike |
| 58 | Guns of Boom Online PvP Action | com.gameinsight.gobandroid |
| 59 | Pacific warships | com.gdcompany.deepwaters |
| 60 | Metal Madness PvP: Car Shooter | com.gdcompany.metalmadness |
| 61 | Steel Rage: Mech Cars PvP War | com.gdcompany.robocars.shooterwarfare |
| 62 | Pirate Code - PVP Battles at Sea | com.happyfish.piratecode |
| 63 | MaskGun: FPS Shooting Gun Game | com.junesoftware.maskgun |
| 64 | Combat of CyberSphere: Online | com.lb4business.cybersphereonline |
| 65 | Mech Wars - Online Battles | com.momend.mechwars |
| 66 | Warface GO: FPS Shooting game | com.my.warface.online.fps.pvp.action.shooter |
| 67 | Knives Out | com.netease.ko |
| 68 | Arena of Valor | com.ngame.allstar.eu |
| 69 | KUBOOM 3D: FPS Shooter | com.Nobodyshot.kuboom |
| 70 | Tacticool | com.panzerdog.tacticool |
| 71 | Pixel Gun 3D - Battle Royale | com.pixel.gun3d |
| 72 | War Robots Multiplayer Battles | com.pixonic.wwr |
| 73 | Mech Arena: Robot Showdown | com.plarium.mechlegion |
| 74 | Evil Lands: Online Action RPG | com.ragequitgames.evillands |
| 75 | Massive Warfare: Tanks Battle | com.tinybytes.massivewarfare2 |
| 76 | Tuning Club Online | com.twoheadedshark.tco |
| 77 | Cyberika: Action Cyberpunk RPG | game.rpg.action.cyber |
| 78 | Sky Combat: War Planes Onlines | shooter.online.warplanes |
| 79 | Frostborn: Action RPG | valhalla.survival.craft.z |
| 80 | Modern Ops: Gun Shooting Games | com.edkongames.mobs |
| 81 | Pokemon Unite | jp.pokemon.pokemonunite |
| 82 | PUBG mobile | com.tencent.ig |
| 83 | Dragon Raja | com.zloong.eu.dr.gp |
| 84 | FOG MOBA Battle Royale Game | pvp.survival.rpg.fog |
| 85 | Gaia Odyssey | com.eyougame.xjhx.en |
| 86 | Marvel Future Fight | com.netmarble.mherosgb |
| 87 | Sniper Arena | com.nordcurrent.sniperarena |
| 88 | Dead Effect 2 | com.badflyinteractive.deadeffect2 |
| 89 | Black Dessert mobile | com.pearlabyss.blackdesertm.gl |
| 90 | Warships Universe | com.gamespire.warships |
| 91 | Robots vs Tanks: 5v5 Battle | com.extremedevelopers.tanksvsrobots |
| 92 | Yokai tamer | com.eyougame.yokaitamer.en |
| 93 | The Tiger | com.swiftappskom.thetigerrpg |
| 94 | The Wolf | com.swiftappskom.thewolfrpg |
| 95 | The walking Zombie 2 | com.aldagames.zombieshooter |
| 96 | Battle force | battle.shooter.fps.online.game |
| 97 | Lineage2: Revolution | com.netmarble.lin2ws |
| 98 | EpicFantasy | net.cravemob.epicfantasy |
| 99 | DeathMatch | com.AntiGame.DeathMatch |
| 100 | Darkness Rises | com.nexon.da3.global |

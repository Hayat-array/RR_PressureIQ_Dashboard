import csv, math
from pathlib import Path

BASE = Path(__file__).parent
input_file = BASE / "data" / "RR_PressureIQ_Full_Candidate_Rankings.csv"
output_file = BASE / "data" / "RR_PressureIQ_Enriched_Candidates.csv"

with open(input_file, encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

# Base overseas roster
overseas_roster = {
    'Donovan Ferreira': ('South Africa', 'Finisher / Power Hitter', 'RHB', 'Right-arm Off-break', 3.0, 'Finisher #6/7 & Backup Keeper', 94, 'Death Overs (16-20)', 'Elite +80.9 SR uplift in late overs; prime lower-order finisher target for RR.'),
    'Tristan Stubbs': ('South Africa', 'Middle-Order Striker / Finisher', 'RHB', 'Right-arm Off-break', 10.0, 'Multi-Phase Match Winner', 96, 'Middle & Death (11-20)', 'Proven IPL spin destroyer and 360 finisher with 79% match consistency.'),
    'Rassie van der Dussen': ('South Africa', 'Middle-Order Anchor', 'RHB', 'Right-arm Leg-break', 2.0, 'Innings Stabilizer', 68, 'Middle Overs (7-15)', 'Reliable accumulator but moderate strike-rate upside under extreme pressure.'),
    'David Miller': ('South Africa', 'Elite Death Finisher', 'LHB', 'Right-arm Off-break', 8.5, 'Clutch Finishing Champion', 93, 'Death Overs (16-20)', 'World-class clutch pedigree with unmatched calm in last-over chases.'),
    'Reeza Hendricks': ('South Africa', 'Top-Order Anchor', 'RHB', 'Right-arm Medium', 2.0, 'Powerplay Anchor', 62, 'Powerplay (1-6)', 'Steady top-order anchor; lower utility for RR aggressive blueprint.'),
    'Aiden Markram': ('South Africa', 'Middle-Order Batter / Off-Spin', 'RHB', 'Right-arm Off-break', 8.0, 'Middle Order Control & Leadership', 85, 'Middle Overs (7-15)', 'Technically compact, handles spin and pace with equal assurance.'),
    'Heinrich Klaasen': ('South Africa', 'Elite Spin Destroyer / Keeper', 'RHB', 'Right-arm Off-break', 15.0, 'World-Class Middle-Overs Aggressor', 99, 'Middle & Death (9-20)', 'Unrivalled destruction of spin; highest impact middle-overs batter in T20 cricket.'),
    'Rilee Rossouw': ('South Africa', 'Aggressive Top-3 Striker', 'LHB', 'Right-arm Off-break', 4.0, 'Fast-Paced Boundary Striker', 74, 'Powerplay & Middle (1-12)', 'High variance boundary hitter against pace.'),
    'Dewald Brevis': ('South Africa', 'Explosive Young Striker', 'RHB', 'Right-arm Leg-break', 4.5, 'High-Ceiling Future Phenom', 85, 'Middle Overs (7-15)', 'Generational boundary hitting ceiling with growing situational maturity.'),
    'Faf du Plessis': ('South Africa', 'Veteran Opener & Captain', 'RHB', 'Right-arm Leg-break', 7.0, 'Powerplay Intent & Leadership', 82, 'Powerplay & Middle (1-12)', 'Consistently aggressive powerplay tempo setter.'),
    'Lungi Ngidi': ('South Africa', 'Hard-Length Fast Bowler', 'RHB', 'Right-arm Fast', 3.5, 'Middle-Overs Hit-the-Deck Pacer', 78, 'Powerplay & Death', 'Tall bowler extracting heavy bounce on hard lengths.'),
    'Gerald Coetzee': ('South Africa', 'Express Middle-Overs Enforcer', 'RHB', 'Right-arm Fast', 6.0, '145kph+ Hostile Pace Weapon', 86, 'Middle & Death (11-20)', 'Enforcer who rattles batters with raw pace and aggressive short balls.'),
    'Marco Jansen': ('South Africa', 'Tall Left-Arm Pacer & Batter', 'RHB', 'Left-arm Fast', 7.5, 'New-Ball Bounce & Lower Order Runs', 88, 'Powerplay & Death', 'High-release left-arm bounce with dangerous lower-order hitting.'),
    'Anrich Nortje': ('South Africa', 'Express 150kph Strike Bowler', 'RHB', 'Right-arm Fast', 6.5, 'Extreme Pace Impact', 82, 'Middle & Death (11-20)', 'Outright speed to blast through middle overs.'),
    'Kagiso Rabada': ('South Africa', 'Marquee Fast Bowling Leader', 'RHB', 'Right-arm Fast', 11.5, 'High-Impact Multi-Phase Pacer', 92, 'Multi-Phase Core', 'Elite multi-phase spearhead with championship-winning pedigree.'),
    'Matheesha Pathirana': ('Sri Lanka', 'Elite Slinger / Death Over Maestro', 'RHB', 'Right-arm Fast (Sling)', 12.5, 'RR #1 Bowling Priority: Lock Overs 18 & 20', 99, 'Death Overs (16-20)', 'The ultimate death-bowling solution; unpickable round-arm yorkers at 150kph.'),
    'Eshan Malinga': ('Sri Lanka', 'Emerging Slinger / Yorker Specialist', 'RHB', 'Right-arm Fast (Sling)', 2.5, 'High-Value Slinger Arbitrage', 92, 'Death Overs (16-20)', 'Sensational value pick; slinging action produces extreme yorker compression under pressure.'),
    'Maheesh Theekshana': ('Sri Lanka', 'Mystery Spinner / Powerplay Choker', 'RHB', 'Right-arm Off-break / Carrom', 7.0, 'Sub-7 Economy & Powerplay Control', 91, 'Powerplay & Middle (1-14)', 'Deadly carrom ball creates boundary drought in powerplay and death.'),
    'Dasun Shanaka': ('Sri Lanka', 'Lower-Order Finisher / Seam', 'RHB', 'Right-arm Medium', 2.0, 'Late-Innings Power', 68, 'Death Overs (16-20)', 'Capable finisher with useful seam bowling backup.'),
    'Bhanuka Rajapaksa': ('Sri Lanka', 'Aggressive Left-Hand Striker', 'LHB', 'None', 2.5, 'Powerplay & Spin Disrupter', 74, 'Powerplay (1-6)', 'Explosive start against pace inside the field restrictions.'),
    'Pathum Nissanka': ('Sri Lanka', 'Technique Top-Order Anchor', 'RHB', 'None', 3.0, 'Solid Anchor Base', 66, 'Powerplay & Middle (1-14)', 'Classical strokeplay with steady boundary accumulation.'),
    'Charith Asalanka': ('Sri Lanka', 'Middle-Order Left-Hander', 'LHB', 'Right-arm Off-break', 2.5, 'Spin Enforcer', 70, 'Middle Overs (7-15)', 'Aggressive against off-spin and left-arm orthodox.'),
    'Kamindu Mendis': ('Sri Lanka', 'Ambidextrous All-Rounder', 'LHB', 'Right/Left-arm Spin', 3.5, 'Rare Ambidextrous Utility', 82, 'Middle Overs (7-15)', 'Tactical chameleon bowling both right-arm off-break and left-arm orthodox.'),
    'Wanindu Hasaranga': ('Sri Lanka', 'World-Class Leg-Spin Wicket Taker', 'RHB', 'Right-arm Leg-break', 10.0, 'Elite Strike Spinner & Finisher', 95, 'Middle Overs (7-15)', 'Premier wicket-taking spinner with lethal googly and lower-order power.'),
    'Dushmantha Chameera': ('Sri Lanka', 'High-Pace Hit-the-Deck Bowler', 'RHB', 'Right-arm Fast', 2.5, 'Express Seam Option', 72, 'Powerplay & Middle', 'Skiddy pace and sharp bounce when fully fit.'),
    'Nuwan Thushara': ('Sri Lanka', 'Malinga-Action Yorker Specialist', 'RHB', 'Right-arm Fast (Sling)', 4.0, 'Death Yorker Precision', 88, 'Death Overs (16-20)', 'Low arm release swings late into the blockhole; excellent death specialist.'),
    'Tim David': ('Australia', 'Express Power Finisher', 'RHB', 'Right-arm Off-break', 8.5, 'Death Overs Power Hitter #6', 90, 'Death Overs (16-20)', 'Monstrous bat speed clearing long boundaries under 12+ RRR.'),
    'Glenn Maxwell': ('Australia', '360° Dynamic All-Rounder', 'RHB', 'Right-arm Off-break', 11.0, 'Middle-Overs Game Breaker', 92, 'Middle & Death (7-20)', 'Game-changing switch hits and tight off-spin powerplay overs.'),
    'Matthew Wade': ('Australia', 'Wicketkeeper Finisher', 'LHB', 'Right-arm Medium', 2.0, 'Pace Hitting Finisher', 70, 'Death Overs (16-20)', 'Experienced ramp and scoop specialist in close chases.'),
    'Marcus Stoinis': ('Australia', 'Power All-Rounder', 'RHB', 'Right-arm Medium-Fast', 9.0, 'Match-Winning Finisher & Seam', 91, 'Middle & Death (11-20)', 'Proven IPL match-winner with brutish power down the ground.'),
    'David Warner': ('Australia', 'Veteran Explosive Opener', 'LHB', 'Right-arm Leg-break', 5.0, 'High-Impact Powerplay Opener', 78, 'Powerplay (1-6)', 'Legendary IPL run-machine with fierce cut and pull shots.'),
    'Cameron Green': ('Australia', 'Pace-Bowling Top-Order All-Rounder', 'RHB', 'Right-arm Fast-Medium', 13.0, 'Rare High-Value Pace All-Rounder', 95, 'Powerplay & Middle', 'Rare tall pace all-rounder; accelerates against express fast bowling.'),
    'Mitchell Marsh': ('Australia', 'Aggressive Top-3 All-Rounder', 'RHB', 'Right-arm Fast-Medium', 8.5, 'Hostile Boundary Striker', 87, 'Powerplay (1-6)', 'Punishes hard lengths with brutal front-foot strikes.'),
    'Josh Inglis': ('Australia', 'Dynamic 360° Keeper Batter', 'RHB', 'None', 5.5, 'Elite Spin/Pace Counter-Attacker', 89, 'Middle & Death (7-20)', 'Highly versatile batter with sweeps, reverse ramps, and composure.'),
    'Mitchell Starc': ('Australia', 'Marquee Left-Arm Express Pacer', 'LHB', 'Left-arm Fast', 13.0, 'Big-Match Weapon & Swing', 88, 'Powerplay & Death', 'Clutch finals performer who swings the white ball at 145kph.'),
    'Nathan Ellis': ('Australia', 'Specialist Death Bowler', 'RHB', 'Right-arm Fast-Medium', 5.5, 'Deceptive Slower Balls & Wide Yorkers', 93, 'Death Overs (16-20)', 'Exceptional cricket IQ at the death with dipping cutters and wide lines.'),
    'Riley Meredith': ('Australia', 'Express Outright Fast Bowler', 'RHB', 'Right-arm Fast', 3.0, 'Outright 145kph+ Pace', 74, 'Middle Overs (7-15)', 'Enforcer who tests helmet badges with raw velocity.'),
    'Sean Abbott': ('Australia', 'Seam Bowling All-Rounder', 'RHB', 'Right-arm Fast-Medium', 2.5, 'Lower-Order Depth & Seam', 72, 'Middle & Death', 'Smart change of pace and reliable lower-order runs.'),
    'Xavier Bartlett': ('Australia', 'Swing & Seam Enforcer', 'RHB', 'Right-arm Fast-Medium', 4.0, 'New-Ball Swing Specialist', 84, 'Powerplay (1-6)', 'High-class outswing and seam presentation in powerplay overs.'),
    'Josh Hazlewood': ('Australia', 'Elite Test-Length Control Bowler', 'LHB', 'Right-arm Fast-Medium', 9.5, 'Pinpoint Metronomic Accuracy', 92, 'Powerplay & Death', 'Immaculate test-match lengths that starve batters of boundary balls.'),
    'Patrick Cummins': ('Australia', 'Marquee Leader & Fast Bowler', 'RHB', 'Right-arm Fast', 14.0, 'Hard-Length Enforcer & Leadership', 90, 'Multi-Phase Core', 'Championship-winning captain with lethal cutters and boundary hitting.'),
    'Jason Behrendorff': ('Australia', 'Left-Arm Powerplay Swing Specialist', 'RHB', 'Left-arm Fast-Medium', 3.5, 'New-Ball Left-Arm Swing', 84, 'Powerplay (1-6)', 'Consistent swing bowler who breaches defences inside the first 3 overs.'),
    'Liam Livingstone': ('England', 'Explosive Boundary Striker / Spin', 'RHB', 'Right-arm Leg/Off-break', 9.0, 'Unrivalled Boundary Hitting', 89, 'Middle & Death (9-20)', 'Pure brute force hitting and bowling both leg-spin and off-spin.'),
    'Harry Brook': ('England', 'Aggressive Middle-Order Batter', 'RHB', 'Right-arm Medium', 7.5, 'Pace Hitting Prowess', 81, 'Middle Overs (7-15)', 'Terrific hand speed against high pace; still developing vs mystery spin.'),
    'Phil Salt': ('England', 'Ultra-Aggressive Keeper Opener', 'RHB', 'None', 9.5, '200+ SR Powerplay Beast', 88, 'Powerplay (1-6)', 'Demolishes powerplay attacks with fearless front-foot strokeplay.'),
    'Jos Buttler': ('England', 'Elite Wicketkeeper Opener', 'RHB', 'None', 14.0, 'RR Legacy Icon & Anchor-Aggressor', 99, 'Powerplay to Death (1-20)', 'Rajasthan Royals legendary cornerstone; can win any chase single-handedly.'),
    'Jacob Bethell': ('England', 'Emerging Left-Hand All-Rounder', 'LHB', 'Slow Left-arm', 3.5, 'Young Dynamic Spin-Hitter', 83, 'Middle Overs (7-15)', 'Fluid stroke maker with fearless temperament in clutch international fixtures.'),
    'Moeen Ali': ('England', 'All-Rounder / Spin Enforcer', 'LHB', 'Right-arm Off-break', 4.5, 'Left-Hand Matchup & Control Spin', 80, 'Middle Overs (7-15)', 'Effortless boundary striker against spin and economical powerplay bowler.'),
    'William Jacks': ('England', 'High-Strike-Rate Top Order / Off-Spin', 'RHB', 'Right-arm Off-break', 7.0, 'Powerplay Boundary Machine', 87, 'Powerplay (1-6)', 'Destructive boundary hitting at 170+ SR in early overs.'),
    'Jonny Bairstow': ('England', 'Explosive Keeper Batter', 'RHB', 'None', 7.0, 'Pace Demolisher', 82, 'Powerplay (1-6)', 'Fearless opener tearing into opening bowlers with aggressive pull shots.'),
    'Sam Curran': ('England', 'Left-Arm All-Rounder', 'LHB', 'Left-arm Medium-Fast', 10.0, 'Death Overs Variations & Lower Runs', 89, 'Multi-Phase Core', 'Competitive fighter with wide yorkers, knuckle-balls and clutch lower order runs.'),
    'Reece Topley': ('England', 'Tall Left-Arm Swing Bowler', 'RHB', 'Left-arm Fast-Medium', 4.0, 'Steep Bounce & New Ball Swing', 83, 'Powerplay & Middle', 'Awkward angle and steep bounce from 6ft 7in frame.'),
    'Jofra Archer': ('England', 'Express 150kph Strike Bowler', 'RHB', 'Right-arm Fast', 9.5, 'RR Former MVP: Hostile Pace', 91, 'Powerplay & Death', 'RR MVP pedigree; hostile bouncers and 150kph reverse swing.'),
    'Chris Jordan': ('England', 'Death Over Specialist & Fielder', 'RHB', 'Right-arm Fast-Medium', 2.5, 'Death Overs Experience', 72, 'Death Overs (16-20)', 'Specialist yorker execution with world-class outfield catching.'),
    'Romario Shepherd': ('West Indies', 'Fast-Bowling Power Finisher', 'RHB', 'Right-arm Fast-Medium', 5.5, 'Late Over Carnage & 138kph Seam', 88, 'Death Overs (16-20)', 'Devastating 30-run-over potential in the 20th over.'),
    'Kieron Pollard': ('West Indies', 'Legendary Power Finisher', 'RHB', 'Right-arm Medium', 2.5, 'Experience & Clutch Power', 70, 'Death Overs (16-20)', 'Master tactician who reads high-pressure chase equations perfectly.'),
    'Jason Holder': ('West Indies', 'Tall Seamer & Long-Lever Hitter', 'RHB', 'Right-arm Fast-Medium', 4.5, 'Balance & Heavy Lengths', 76, 'Powerplay & Death', 'Height provides heavy lengths and dependable catching at long-on.'),
    'Sherfane Rutherford': ('West Indies', 'Left-Hand Clutch Finisher', 'LHB', 'Right-arm Fast-Medium', 5.0, 'Clutch Finishing Against High Pace', 91, 'Death Overs (16-20)', 'Specialist in resurrecting chases from precarious positions.'),
    'Shai Hope': ('West Indies', 'Middle-Order Keeper Anchor', 'RHB', 'None', 2.5, 'Spin Playing Stabilizer', 66, 'Middle Overs (7-15)', 'Calculated accumulator who anchors collapsing batting orders.'),
    'Nicholas Pooran': ('West Indies', 'Elite Left-Hand Finisher', 'LHB', 'Right-arm Off-break', 14.5, 'World-Class Spin Destroyer', 98, 'Middle & Death (9-20)', 'Best six-hitter in white ball cricket; annihilates spin effortlessly.'),
    'Rovman Powell': ('West Indies', 'Power Finisher & Boundary Striker', 'RHB', 'Right-arm Medium-Fast', 6.5, 'RR Power Hitter #6', 87, 'Death Overs (16-20)', 'Proven RR finisher with explosive straight-down-the-ground power.'),
    'Shimron Hetmyer': ('West Indies', 'Elite Death-Overs Finisher', 'LHB', 'None', 9.0, 'RR Core Match Winner', 96, 'Death Overs (16-20)', 'The heart of RR finishing lineup; ice-cold under 12+ RRR equations.'),
    'Andre Russell': ('West Indies', 'Match-Winning All-Rounder', 'RHB', 'Right-arm Fast', 12.0, 'Max Firepower & Clutch Yorker Seam', 95, 'Death Overs (16-20)', 'Unstoppable boundary beast who also bowls 140kph clutch death overs.'),
    'Roston Chase': ('West Indies', 'Spin Bowling All-Rounder', 'RHB', 'Right-arm Off-break', 1.5, 'Economical Middle Overs Spin', 66, 'Middle Overs (7-15)', 'Defensive off-spinner who constricts run-rates.'),
    'Sunil Narine': ('West Indies', 'Legendary Mystery Spinner & Opener', 'LHB', 'Right-arm Off-break', 11.0, 'Sub-7 Economy & High-Leverage Master', 94, 'Multi-Phase Core', 'T20 royalty; virtually unhittable economy and ruthless powerplay hitting.'),
    'Obed McCoy': ('West Indies', 'Left-Arm Slower Ball Specialist', 'LHB', 'Left-arm Fast-Medium', 3.0, 'Back-of-Hand Slower Balls', 80, 'Death Overs (16-20)', 'Tricky back-of-the-hand slower balls and angled cutters for RR.'),
    'Shamar Joseph': ('West Indies', 'Hostile 150kph Express Pacer', 'RHB', 'Right-arm Fast', 4.5, 'Fearless Outright Pace', 84, 'Powerplay & Middle', 'Raw heart and 150kph thunderbolts that push batters back.'),
    'Alzarri Joseph': ('West Indies', 'Express High-Bounce Pacer', 'RHB', 'Right-arm Fast', 4.0, 'Hard Lengths 145kph+', 78, 'Middle Overs (7-15)', 'Aggressive bounce targeting the ribcage of middle-order batters.'),
    'Babar Azam': ('Pakistan', 'Top-Order Anchor', 'RHB', 'Right-arm Off-break', 5.0, 'Top-Order Stability', 60, 'Powerplay & Middle', 'High classical average but strike-rate limitation in extreme IPL chases.'),
    'Fakhar Zaman': ('Pakistan', 'High-Intent Left-Hand Opener', 'LHB', 'Slow Left-arm', 3.5, 'Aggressive Powerplay Opener', 66, 'Powerplay (1-6)', 'Fearless pull shot against high pace in early overs.'),
    'Mohammad Rizwan': ('Pakistan', 'Wicketkeeper Anchor', 'RHB', 'None', 5.0, 'Tenacious Chase Anchor', 62, 'Powerplay & Middle', 'Tireless running between wickets and sweep shots.'),
    'Salman Agha': ('Pakistan', 'Middle-Order Batter / Off-Spin', 'RHB', 'Right-arm Off-break', 2.0, 'Utility Middle Order', 60, 'Middle Overs (7-15)', 'Steady accumulator and part-time off-spin.'),
    'Imad Wasim': ('Pakistan', 'Powerplay Left-Arm Spinner & Finisher', 'LHB', 'Slow Left-arm Orthodox', 3.0, 'Stifling Powerplay Economy', 78, 'Powerplay & Death', 'Skiddy round-arm darts with excellent powerplay control.'),
    'Usman Khan': ('Pakistan', 'Aggressive Top-3 Striker', 'RHB', 'Right-arm Off-break', 2.0, 'High-SR Boundary Striker', 68, 'Powerplay (1-6)', 'High boundary percentage in franchise leagues.'),
    'Shadab Khan': ('Pakistan', 'Leg-Spin All-Rounder', 'RHB', 'Right-arm Leg-break', 4.5, 'Middle-Overs Leg Spin & Power Hitting', 76, 'Middle Overs (7-15)', 'Skiddy leg-spin and counter-attacking bat speed.'),
    'Mohammad Nawaz': ('Pakistan', 'Left-Arm Spinner & Batter', 'LHB', 'Slow Left-arm', 2.0, 'Matchup Left-Arm Spin', 65, 'Middle Overs (7-15)', 'Matchup weapon against right-hand heavy batting orders.'),
    'Iftikhar Ahmed': ('Pakistan', 'Power Hitter & Off-Spin', 'RHB', 'Right-arm Off-break', 2.5, 'Spin Demolisher', 70, 'Death Overs (16-20)', 'Heavy ball-striking over deep mid-wicket against spin.'),
    'Khushdil Shah': ('Pakistan', 'Left-Hand Lower-Order Striker', 'LHB', 'Slow Left-arm', 1.5, 'Boundary Finisher', 62, 'Death Overs (16-20)', 'Finisher with slog-sweep power.'),
    'Haris Rauf': ('Pakistan', 'Express Fast Bowler / Death Enforcer', 'RHB', 'Right-arm Fast', 6.5, '150kph High-Leverage Yorker Machine', 84, 'Middle & Death (11-20)', '150kph thunderbolts and searing yorkers under pressure.'),
    'Shaheen Afridi': ('Pakistan', 'Elite Left-Arm Fast Swing Bowler', 'LHB', 'Left-arm Fast', 7.5, 'Destructive 1st Over Wicket Weapon', 82, 'Powerplay (1-6)', 'Lethal full inswing hitting front pads in over 1.'),
    'Naseem Shah': ('Pakistan', 'Lethal Pace & Seam Bowler', 'RHB', 'Right-arm Fast', 6.0, 'High-Speed Seam Movement', 82, 'Powerplay & Death', 'Pristine seam presentation and blistering pace in clutch fixtures.'),
    'Trent Boult': ('New Zealand', 'Elite Left-Arm Swing Weapon', 'RHB', 'Left-arm Fast-Medium', 10.0, 'RR Iconic Powerplay Wicket Taker', 97, 'Powerplay (1-6)', 'RR franchise legend; holds the record for most first-over IPL wickets.'),
    'Mark Chapman': ('New Zealand', 'Middle-Order Left-Hander', 'LHB', 'Slow Left-arm', 2.0, 'Spin Sweeper & Floater', 68, 'Middle Overs (7-15)', 'Innovative sweeps against spin; smart rotation.'),
    'Daryl Mitchell': ('New Zealand', 'Middle-Overs Spin Destroyer', 'RHB', 'Right-arm Medium', 7.5, 'Clutch Knockout Match Performer', 89, 'Middle Overs (7-15)', 'Elite temperament in big tournaments; dominates straight ground.'),
    'Devon Conway': ('New Zealand', 'High-Consistency Keeper Opener', 'LHB', 'Right-arm Medium', 7.0, 'Unbreakable Top-Order Anchor', 86, 'Powerplay & Middle', 'Master of finding gaps and building match-winning totals.'),
    'Mitchell Santner': ('New Zealand', 'Sub-7 Economy Finger Spinner', 'LHB', 'Slow Left-arm Orthodox', 5.5, 'Stifling Middle-Overs Control', 89, 'Middle Overs (7-15)', 'Unflappable control and suffocating middle-overs economy.'),
    'Rachin Ravindra': ('New Zealand', 'All-Rounder / Top-Order Striker', 'LHB', 'Slow Left-arm', 7.0, 'Left-Hand Powerplay Striker & Spin', 88, 'Powerplay & Middle', 'Silky strokeplay with rapid boundary progression.'),
    'Jimmy Neesham': ('New Zealand', 'Clutch Finisher & Seam Option', 'LHB', 'Right-arm Medium-Fast', 2.5, 'High-Leverage Boundary Striker', 81, 'Death Overs (16-20)', 'High-impact lower-order cameos in tight finishes.'),
    'Glenn Phillips': ('New Zealand', 'Dynamic 360° Finisher / Keeper', 'RHB', 'Right-arm Off-break', 6.5, 'Extraordinary Fielding & Power Hitter', 91, 'Middle & Death (7-20)', 'Superhuman fielder, dynamic finisher, and useful off-spinner.'),
    'Adam Milne': ('New Zealand', 'Express Fast Bowler', 'RHB', 'Right-arm Fast', 2.5, 'Outright 145kph Pace', 75, 'Middle & Death', 'Extreme pace through the air when fit.'),
    'Tim Southee': ('New Zealand', 'Veteran Swing & Seam Bowler', 'RHB', 'Right-arm Fast-Medium', 2.0, 'New-Ball Seam Control', 70, 'Powerplay & Death', 'Experienced campaigner with smart knuckle-balls and wide yorkers.'),
    'Matt Henry': ('New Zealand', 'Pinpoint Powerplay Seam Bowler', 'RHB', 'Right-arm Fast-Medium', 4.0, 'Upright Seam & Early Wickets', 85, 'Powerplay (1-6)', 'One of the best new-ball seam bowlers in world cricket.'),
    'Kyle Jamieson': ('New Zealand', 'Giant Tall Fast Bowler', 'RHB', 'Right-arm Fast-Medium', 3.0, 'Steep Uncomfortable Bounce', 75, 'Powerplay & Middle', 'Extreme height generates awkward bounce from good length.'),
    'Jacob Duffy': ('New Zealand', 'Reliable Outswing Pacer', 'RHB', 'Right-arm Fast-Medium', 1.5, 'Disciplined Line & Length', 70, 'Powerplay (1-6)', 'Classic swing bowler with strong domestic credentials.'),
    'Lockie Ferguson': ('New Zealand', '150kph Express Fast Bowler', 'RHB', 'Right-arm Fast', 5.0, 'Extreme Pace & Heavy Ball', 83, 'Middle & Death (11-20)', '150kph enforcer who destroys stumps with sheer speed.'),
    'Najibullah Zadran': ('Afghanistan', 'Left-Hand Lower-Order Power Hitter', 'LHB', 'Right-arm Off-break', 1.5, 'Pace Hitting Specialist', 74, 'Death Overs (16-20)', 'Left-hand power hitting against express pace.'),
    'Ibrahim Zadran': ('Afghanistan', 'Top-Order Anchor', 'RHB', 'Right-arm Medium', 2.0, 'Composed Anchor', 65, 'Powerplay & Middle', 'Solid defensive technique and building partnerships.'),
    'Azmatullah Omarzai': ('Afghanistan', 'Pace Bowling All-Rounder', 'RHB', 'Right-arm Fast-Medium', 5.0, 'High-Utility Seam All-Rounder', 84, 'Middle & Death', 'Modern seam-bowling all-rounder who strikes clean straight sixes.'),
    'Mohammad Nabi': ('Afghanistan', 'Veteran All-Rounder & Finisher', 'RHB', 'Right-arm Off-break', 2.5, 'Experienced Spin & Power', 75, 'Middle & Death', 'Calm head and smart tactical off-spin match-ups.'),
    'Karim Janat': ('Afghanistan', 'Lower-Order Striker & Seam', 'RHB', 'Right-arm Medium', 1.0, 'Depth Utility', 64, 'Death Overs (16-20)', 'Aggressive boundary seeker.'),
    'Naveen ul Haq': ('Afghanistan', 'Death Slower Ball Specialist', 'RHB', 'Right-arm Medium-Fast', 4.5, 'Deceptive Slower Balls & Yorkers', 84, 'Death Overs (16-20)', 'Dipping back-of-the-hand slower balls and yorkers.'),
    'Rashid Khan': ('Afghanistan', 'World No. 1 T20 Spinner', 'RHB', 'Right-arm Leg-break', 16.0, 'Unrivalled Control & Clutch Match Winner', 99, 'Multi-Phase Core', 'T20 GOAT; impenetrable economy and match-winning sixes at #8.'),
    'FazalHaq Farooqi': ('Afghanistan', 'Left-Arm Powerplay Swing Bowler', 'RHB', 'Left-arm Fast-Medium', 4.5, 'Sharp Early Inswing', 85, 'Powerplay (1-6)', 'Lethal swinging ball into the pads of right-handers in powerplay.'),
    'Gareth Delany': ('Ireland', 'Lower-Order Striker / Leg-spinner', 'RHB', 'Right-arm Leg-break', 1.0, 'High-Risk Boundary Accelerator', 72, 'Death Overs (16-20)', 'Elite +71.9 SR delta; explosive lower-order boundary accelerator.'),
    'Harry Tector': ('Ireland', 'Composed Middle-Order Batter', 'RHB', 'Right-arm Off-break', 1.0, 'Classical Middle-Overs Floater', 65, 'Middle Overs (7-15)', 'Compact technique against elite pace.'),
    'George Dockrell': ('Ireland', 'Hard-Hitting Finisher & Spinner', 'RHB', 'Slow Left-arm', 0.8, 'Lower-Order Power Upgrade', 68, 'Death Overs (16-20)', 'Transformed into a heavy-hitting power finisher.'),
    'Lorcan Tucker': ('Ireland', 'Dynamic Keeper Batter', 'RHB', 'None', 1.0, '360° Ramp & Lap Specialist', 72, 'Middle & Death (7-20)', 'Fearless lap and ramp hitter against fast bowlers.'),
    'Curtis Campher': ('Ireland', 'Aggressive All-Rounder', 'RHB', 'Right-arm Fast-Medium', 1.5, 'Tenacious Competitive Fighter', 76, 'Middle & Death', 'Hat-trick hero with ferocious competitive fight in tight games.'),
    'Joshua Little': ('Ireland', 'Left-Arm Fast-Medium Bowler', 'RHB', 'Left-arm Fast-Medium', 3.0, 'Hard Lengths & Left-Arm Angle', 78, 'Powerplay & Middle', 'Brings high release and angle from over the wicket.'),
    'Mark Adair': ('Ireland', 'New-Ball Swing & Death Bowler', 'RHB', 'Right-arm Fast-Medium', 1.5, 'Wicket-Taking Seamer & Hitter', 74, 'Powerplay & Death', 'High wicket frequency with late outswing.'),
    'Barry McCarthy': ('Ireland', 'Hit-the-Deck Fast-Medium', 'RHB', 'Right-arm Fast-Medium', 0.75, 'Aggressive Length Seamer', 66, 'Middle Overs (7-15)', 'Aggressive enforcer length bowling.'),
    'Sikandar Raza': ('Zimbabwe', 'Spin Bowling All-Rounder & Match Winner', 'RHB', 'Right-arm Off-break', 4.0, 'High-Leverage Clutch Hero', 88, 'Middle & Death (7-20)', 'Clutch performer who elevates game in high-stakes pressure situations.'),
    'Ryan Burl': ('Zimbabwe', 'Left-Hand Finisher & Leg Spinner', 'LHB', 'Right-arm Leg-break', 1.0, 'Boundary Striker & Spin', 72, 'Death Overs (16-20)', 'Clean ball striker against pace and spin.'),
    'Wesley Madhevere': ('Zimbabwe', 'Top-Order Batter / Off-Spin', 'RHB', 'Right-arm Off-break', 0.5, 'Young Anchor', 60, 'Powerplay (1-6)', 'Young stroke maker.'),
    'Clive Madande': ('Zimbabwe', 'Keeper Finisher', 'RHB', 'None', 0.5, 'Lower-Order Keeper', 58, 'Death Overs (16-20)', 'Tenacious lower-order keeper.'),
    'Tashinga Musekiwa': ('Zimbabwe', 'Lower-Order Power Finisher', 'RHB', 'Right-arm Medium', 0.5, 'Late-Overs Striker', 64, 'Death Overs (16-20)', 'Big hitter in closing overs.'),
    'Blessing Muzarabani': ('Zimbabwe', 'Tall High-Bounce Express Bowler', 'RHB', 'Right-arm Fast', 2.0, 'Hostile Bounce & Pace', 78, 'Powerplay & Death', '6ft 8in release point generates extreme bounce on good lengths.'),
    'Brad Evans': ('Zimbabwe', 'Death Seam Bowler', 'RHB', 'Right-arm Fast-Medium', 0.75, 'Death Variations', 68, 'Death Overs (16-20)', 'Wide yorkers and competitive death bowling.'),
    'Richard Ngarava': ('Zimbabwe', 'Tall Left-Arm Fast Bowler', 'LHB', 'Left-arm Fast-Medium', 2.0, 'Left-Arm Angle & Bounce', 76, 'Powerplay & Middle', 'Left-arm angle troubling right-hand openers.'),
    'Luke Jongwe': ('Zimbabwe', 'Death Slower Ball Specialist', 'RHB', 'Right-arm Medium-Fast', 0.75, 'Wide Yorkers & Cutters', 66, 'Death Overs (16-20)', 'Deceptive slower balls in the death.'),
    'Jaker Ali Anik': ('Bangladesh', 'Wicketkeeper Finisher', 'RHB', 'None', 0.75, 'Late-Overs Finishing Option', 65, 'Death Overs (16-20)', 'Solid domestic finisher with calm temperament.'),
    'Nurul Hasan': ('Bangladesh', 'Keeper Finisher', 'RHB', 'None', 0.8, 'Lower-Order Keeper', 60, 'Death Overs (16-20)', 'Quick hands behind the stumps and busy runner.'),
    'Towhid Hridoy': ('Bangladesh', 'Aggressive Middle-Order Batter', 'RHB', 'Right-arm Off-break', 1.5, 'Spin Counter-Attacker', 72, 'Middle Overs (7-15)', 'Positive intent against quality spin in middle overs.'),
    'Mahedi Hasan': ('Bangladesh', 'Powerplay Off-Spinner & Batter', 'RHB', 'Right-arm Off-break', 1.5, 'Powerplay Bowling Economy', 74, 'Powerplay (1-6)', 'Specialist in bowling tight lines in the first 6 overs.'),
    'Shamim Hossain': ('Bangladesh', 'Left-Hand Lower-Order Striker', 'LHB', 'Right-arm Off-break', 0.75, 'Boundary Accelerator', 64, 'Death Overs (16-20)', 'Livewire in the field and fearless hitter.'),
    'Afif Hossain': ('Bangladesh', 'Dynamic Left-Hand Batter & Off-Spin', 'LHB', 'Right-arm Off-break', 1.0, 'Left-Hand Middle Order', 68, 'Middle Overs (7-15)', 'Compact left-hander with variety of ramp shots.'),
    'Mohammad Mahmudullah': ('Bangladesh', 'Veteran Finisher / Off-Spin', 'RHB', 'Right-arm Off-break', 1.5, 'Experienced Finisher', 68, 'Death Overs (16-20)', 'Veteran composure when wickets fall.'),
    'Taskin Ahmed': ('Bangladesh', 'Outright 145kph Strike Bowler', 'LHB', 'Right-arm Fast', 3.0, 'High-Pace Hit-the-Deck Seamer', 80, 'Powerplay & Middle', 'Genuinely fast with sharp seam movement off the pitch.'),
    'Mohammad Saifuddin': ('Bangladesh', 'Death Bowler & Hitter', 'LHB', 'Right-arm Medium-Fast', 1.0, 'Yorker Execution & Hitting', 70, 'Death Overs (16-20)', 'Pinpoint yorkers and useful lower order hitting.'),
    'Shoriful Islam': ('Bangladesh', 'Left-Arm Swing & Seam Bowler', 'LHB', 'Left-arm Fast-Medium', 2.0, 'Left-Arm New Ball Swing', 76, 'Powerplay (1-6)', 'Lethal inswing into right handers.'),
    'Mustafizur Rahman': ('Bangladesh', 'Master of Slower Cutters', 'LHB', 'Left-arm Fast-Medium', 4.5, 'Deceptive Gripping Cutters', 86, 'Death Overs (16-20)', 'Legendary off-cutter grips and dies on dry pitches.'),
    'Tanzim Sakib': ('Bangladesh', 'Aggressive Young Fast Bowler', 'RHB', 'Right-arm Fast-Medium', 1.5, 'Sharp Skiddy Pace', 72, 'Powerplay & Middle', 'Fierce competitor who bowls with high intensity.'),
    'Rahul Chopra': ('United Arab Emirates', 'Middle-Order Striker', 'RHB', 'None', 0.5, 'Associate Performer', 55, 'Middle Overs (7-15)', 'Associate talent with promising stroke play.'),
    'Junaid Siddique': ('United Arab Emirates', 'Skiddy Fast Bowler', 'RHB', 'Right-arm Fast-Medium', 0.75, 'Skiddy Pace Option', 64, 'Powerplay & Death', 'Skiddy bouncers and brisk pace.')
}

# Special Indian player mappings
indian_profiles = {
    'Shashank Singh': ('Clutch Finisher / Striker', 'RHB', 'Right-arm Medium', 7.5, 'Elite Domestic Finisher #6', 97, 'Death Overs (16-20)', 'Gold standard domestic clutch performer; +60.1 SR delta over 362 pressure balls!'),
    'Rinku Singh': ('Elite Finisher / Match Winner', 'LHB', 'Right-arm Off-break', 13.0, 'Death-Over Chase Master #5/6', 99, 'Death Overs (16-20)', 'The most dependable chase specialist in Indian cricket; 84.8% match consistency.'),
    'Namboori Tilak Varma': ('Middle-Order Anchor & Striker', 'LHB', 'Right-arm Off-break', 11.5, 'Left-Hand Core Middle Order #4', 94, 'Middle & Death (7-20)', 'Terrific composure under pressure; averages 36.8 at 181 SR in clutch situations.'),
    'Dinesh Karthik': ('Veteran Finisher / Wicketkeeper', 'RHB', 'None', 3.0, 'Tactical Mentor & Clutch Finisher', 65, 'Death Overs (16-20)', 'Experienced finishing specialist with incredible strike-rate elevation.'),
    'Mahendra Singh Dhoni': ('Legendary Finisher / Keeper', 'RHB', 'Right-arm Medium', 4.0, 'Clutch Finishing & Leadership', 70, 'Death Overs (16-20)', 'T20 finishing icon with +82.2 delta over baseline in death overs.'),
    'Shreyas Iyer': ('Middle-Order Anchor & Captain', 'RHB', 'Right-arm Leg-break', 12.0, 'Captaincy & Spin Enforcer', 82, 'Middle Overs (7-15)', 'IPL championship-winning captain; steps up with 195.7 SR under pressure.'),
    'Suryakumar Yadav': ('360° Elite T20 Batter', 'RHB', 'Right-arm Medium', 16.0, 'World-Class Match Winner #3/4', 99, 'Middle & Death (7-20)', 'Unstoppable 360-degree shot-making against any field setting.'),
    'Shubman Gill': ('Elite Top-Order Anchor', 'RHB', 'Right-arm Off-break', 14.0, 'Anchor / Powerplay Control', 80, 'Powerplay & Middle (1-14)', 'Master of pacing 200+ run chases from the top.'),
    'Naman Dhir': ('Aggressive Middle-Overs Striker', 'RHB', 'Right-arm Off-break', 4.0, 'Emerging High-SR Indian Option', 88, 'Middle Overs (7-15)', 'Exciting young Indian power hitter who takes down high pace instantly.'),
    'Sameer Rizvi': ('Spin-Hitting Specialist', 'RHB', 'Right-arm Off-break', 4.0, 'Middle-Overs Aggressor', 78, 'Middle Overs (7-15)', 'Huge raw six-hitting power against spinners in middle overs.'),
    'Jitesh Sharma': ('Wicketkeeper Finisher', 'RHB', 'None', 7.0, 'Indian Keeper-Finisher #6', 91, 'Death Overs (16-20)', 'Ultra-aggressive keeper-finisher who attacks from ball one.'),
    'Ruturaj Gaikwad': ('Top-Order Anchor & Captain', 'RHB', 'Right-arm Off-break', 12.0, 'Powerplay Anchor', 78, 'Powerplay & Middle', 'Calm top-order anchor with magnificent second-half acceleration.'),
    'Vijay Shankar': ('Batting All-Rounder', 'RHB', 'Right-arm Medium', 2.5, 'Middle Order Support', 64, 'Middle Overs (7-15)', 'Experience and steady boundary option.'),
    'Rohit Sharma': ('Marquee Opener & Leader', 'RHB', 'Right-arm Off-break', 13.0, 'Powerplay Striker', 85, 'Powerplay (1-6)', 'Dominant powerplay destroyer with unmatched pull shot.'),
    'Nitish Rana': ('Middle-Order Spin Striker', 'LHB', 'Right-arm Off-break', 6.0, 'Middle Order Left-Hander', 76, 'Middle Overs (7-15)', 'Fearless attack against left-arm orthodox and leg-spin.'),
    'Virat Kohli': ('Elite Marquee Anchor', 'RHB', 'Right-arm Medium', 18.0, 'Chase Master', 88, 'Multi-Phase Core', 'Unprecedented chase mastery and supreme physical running.'),
    'Lokesh Rahul': ('Top-Order Keeper / Anchor', 'RHB', 'None', 13.0, 'Versatile Top-Order Core', 84, 'Powerplay & Middle', 'Impeccable strokeplay with unmatched run-scoring floor.'),
    'Nitish Reddy': ('Pace Bowling All-Rounder', 'RHB', 'Right-arm Medium-Fast', 8.5, 'Rare Indian Fast-Bowling All-Rounder', 96, 'Multi-Phase Core', 'Gold dust profile: 140kph seam bowling + fearless middle-order power hitting.'),
    'Rishabh Pant': ('Marquee Keeper Match-Winner', 'LHB', 'None', 17.0, 'Game-Changing Left-Hand Striker', 96, 'Middle & Death (7-20)', 'One of the most destructive and creative match-winners in T20 history.'),
    'Hardik Pandya': ('Premier Fast-Bowling All-Rounder', 'RHB', 'Right-arm Fast-Medium', 15.0, 'Clutch Finisher & 140kph Seam', 97, 'Multi-Phase Core', 'Championship-winning captain, genuine 140kph death bowler, and elite power finisher.'),
    'Ravindra Jadeja': ('Premier All-Rounder', 'LHB', 'Slow Left-arm', 12.0, 'Clutch Lower-Order & Economical Spin', 92, 'Multi-Phase Core', 'Clutch last-over champion, 6.8 economy, and world best fielder.'),
    'Dhruv Jurel': ('Clutch Keeper Finisher', 'RHB', 'None', 7.5, 'RR Core Clutch Finisher', 96, 'Death Overs (16-20)', 'RR homegrown diamond; extraordinary ice in his veins in tight chases.'),
    'Sanju Samson': ('RR Captain & Elite Striker', 'RHB', 'None', 15.0, 'RR Captain & Cornerstone', 100, 'Powerplay & Middle (1-15)', 'RR Franchise Captain and undisputed cornerstone of Rajasthan Royals.'),
    'Shivam Dube': ('Elite Spin Destroyer', 'LHB', 'Right-arm Medium', 9.5, 'Middle-Overs Pace/Spin Destroyer', 93, 'Middle Overs (7-15)', 'Long levers clear 90m+ sixes against any spinner in the world.'),
    'Riyan Parag': ('Dynamic #4 Batter & Leader', 'RHB', 'Right-arm Leg-break', 11.0, 'RR Homegrown Superstar', 98, 'Middle & Death (7-20)', 'RR talisman; matured into one of the most dominant #4 batters in IPL.'),
    'Rahul Tewatia': ('Specialist Ice-in-Veins Finisher', 'LHB', 'Right-arm Leg-break', 7.5, 'Legendary Clutch Match-Winner', 94, 'Death Overs (16-20)', 'Legendary reputation for winning impossible games in the final 5 balls.'),
    'Jasprit Bumrah': ('Gold-Standard Universal Fast Bowler', 'RHB', 'Right-arm Fast', 18.0, 'Greatest Death Bowler in T20 History', 100, 'Multi-Phase Core', 'The undisputed cheat-code of cricket; economy under 7 in death overs!'),
    'Bhuvneshwar Kumar': ('Veteran Swing & Control Bowler', 'RHB', 'Right-arm Medium-Fast', 4.5, 'Powerplay Knuckle-ball Control', 78, 'Powerplay & Death', 'Master of swing and knuckle-ball slower deliveries.'),
    'Harshal Patel': ('Death-Overs Dipper Specialist', 'RHB', 'Right-arm Medium-Fast', 7.5, 'Slower Ball Dipper in Overs 16-20', 89, 'Death Overs (16-20)', 'Purple Cap winner; deadly dipping slower yorkers deceive modern power hitters.'),
    'T Natarajan': ('Left-Arm Toe-Crusher Yorker Specialist', 'LHB', 'Left-arm Fast-Medium', 8.5, 'Pinpoint Death Overs Yorker Execution', 95, 'Death Overs (16-20)', 'Laser-guided wide and stump yorkers at the death; perfect fit for RR.'),
    'Arshdeep Singh': ('Left-Arm Death & Powerplay Specialist', 'LHB', 'Left-arm Fast-Medium', 13.5, 'Elite Indian Left-Arm Weapon', 98, 'Multi-Phase Core', 'T20 World Cup winner; elite swing up front and cool-headed yorkers at the death.'),
    'Ravi Bishnoi': ('Fast Leg-Spinner & Googly Specialist', 'RHB', 'Right-arm Leg-break', 9.5, 'High-Speed Middle-Overs Wicket Taker', 92, 'Middle Overs (7-15)', 'Brisk 100kph googlies that rush batters; wicket-taker under pressure.'),
    'Yuzvendra Chahal': ('IPL All-Time Wicket Leader & Wizard', 'RHB', 'Right-arm Leg-break', 10.5, 'RR Spin King & Match Winner', 98, 'Middle & Death (7-18)', 'RR legend; all-time leading wicket taker with courage to throw the ball wide.'),
    'Kuldeep Yadav': ('Elite Left-Arm Wrist Spinner', 'LHB', 'Slow Left-arm Chinaman', 12.5, 'Unpickable Middle-Overs Variations', 97, 'Middle Overs (7-15)', 'Unpickable revs on the ball, sharp drift and turn in middle overs.'),
    'Sandeep Sharma': ('RR Death & Swing Specialist', 'RHB', 'Right-arm Medium', 5.5, 'RR Core Clutch Executioner', 96, 'Powerplay & Death', 'RR hero; masters wide yorkers and changes of pace against world best hitters.'),
    'Mohammed Shami': ('Premier Seam Presentation Bowler', 'RHB', 'Right-arm Fast', 11.0, 'Lethal Seam & Upright Powerplay Spells', 92, 'Powerplay & Death', 'Upright seam creates vicious movement and early wickets.'),
    'Mohammed Siraj': ('Hostile Outswing Fast Bowler', 'RHB', 'Right-arm Fast', 9.5, 'Fiery Powerplay Striker', 86, 'Powerplay & Middle', 'Fiery spell-caster who runs through top orders on green surfaces.'),
    'Yash Dayal': ('Left-Arm Swing & Death Bowler', 'LHB', 'Left-arm Fast-Medium', 5.0, 'Resilient Death Yorker Bowler', 84, 'Powerplay & Death', 'Exceptional character, bowls calm wide yorkers in last-over defences.'),
    'Mohsin Khan': ('Tall Left-Arm Fast Bowler', 'LHB', 'Left-arm Fast-Medium', 4.5, 'Steep Bounce & Defending Low Totals', 85, 'Powerplay & Death', 'Tall left-armer who defends 9 runs in final overs with ease.'),
    'Varun Chakravarthy': ('Mystery Spinner & Googly Specialist', 'RHB', 'Right-arm Leg-break / Mystery', 10.0, 'Middle-Overs Stifler', 94, 'Middle Overs (7-15)', 'IPL champion mystery spinner; batters cannot read his carrom release.'),
    'Prasidh Krishna': ('High-Release Express Pacer', 'RHB', 'Right-arm Fast', 6.5, 'RR Tall Express Pacer', 85, 'Middle & Death', 'RR speedster with steep bounce and 145kph burst.')
}

enriched_rows = []
for r in rows:
    # Handle possible BOM in column key
    cat = r.get('category') or r.get('\ufeffcategory')
    name = r['player_name']
    score = float(r['model_score']) if r.get('model_score') else 0.0
    balls = int(r['pressure_balls']) if r.get('pressure_balls') else 0
    matches = int(r['pressure_matches']) if r.get('pressure_matches') else 0
    consistency = float(r['consistency_pct']) if r.get('consistency_pct') else 50.0
    rate = float(r['pressure_strike_rate_or_economy']) if r.get('pressure_strike_rate_or_economy') else 0.0
    delta = float(r['change_vs_baseline']) if r.get('change_vs_baseline') else 0.0
    ipl_balls = int(r['IPL_pressure_balls']) if r.get('IPL_pressure_balls') else 0
    t20i_balls = int(r['T20I_pressure_balls']) if r.get('T20I_pressure_balls') else 0

    if name in overseas_roster:
        country, skill, bat_style, bowl_style, price, role_fit, fit_score, phase, verdict = overseas_roster[name]
        is_overseas = True
    elif name in indian_profiles:
        country = 'India'
        is_overseas = False
        skill, bat_style, bowl_style, price, role_fit, fit_score, phase, verdict = indian_profiles[name]
    else:
        # Default domestic assignment
        country = 'India'
        is_overseas = False
        if cat and cat.lower() == 'batter':
            skill = 'Middle-Overs Striker'
            bat_style = 'RHB'
            bowl_style = 'Right-arm Medium'
            price = round(max(0.5, min(6.0, score * 5.0)), 2)
            role_fit = 'Domestic Batting Depth'
            fit_score = int(max(60, min(88, score * 90)))
            phase = 'Middle Overs (7-15)'
            verdict = f'Solid domestic batting prospect with {rate:.1f} pressure strike rate.'
        else:
            skill = 'Pace Bowler / Seamer'
            bat_style = 'RHB'
            bowl_style = 'Right-arm Fast-Medium'
            price = round(max(0.5, min(6.0, score * 5.0)), 2)
            role_fit = 'Domestic Bowling Depth'
            fit_score = int(max(60, min(88, score * 90)))
            phase = 'Middle & Death'
            verdict = f'Disciplined bowler with {rate:.2f} pressure economy.'

    # Compute Auction Tier
    if score >= 0.88 and ipl_balls >= 100:
        auction_tier = 'Tier 1: Marquee Priority'
    elif score >= 0.70 and delta > (25.0 if cat and cat.lower()=='batter' else -0.5):
        auction_tier = 'Tier 2: High-Value Moneyball'
    elif score >= 0.60:
        auction_tier = 'Tier 3: High-Upside Punt'
    else:
        auction_tier = 'Tier 4: Caution / Trap Risk' if delta < 0 else 'Tier 3: High-Upside Punt'

    # Compute Normalized Radar Metrics (0 to 100 scale)
    if cat and cat.lower() == 'batter':
        r_output = min(100, max(20, int((rate - 120) / (220 - 120) * 80 + 20)))
        r_delta = min(100, max(15, int((delta + 20) / (90 + 20) * 85 + 15)))
    else:
        # For economy: lower is better (e.g. 7.0 is elite, 11.0 is poor)
        r_output = min(100, max(20, int((12.5 - rate) / (12.5 - 6.5) * 80 + 20)))
        r_delta = min(100, max(15, int((-delta + 3.0) / (3.0 + 3.0) * 85 + 15)))

    r_sample = min(100, max(15, int(math.log10(max(10, balls)) / math.log10(700) * 100)))
    r_consistency = min(100, max(20, int(consistency)))
    r_ipl = min(100, max(10, int(min(ipl_balls, 400) / 400 * 90 + 10)))
    r_synergy = int(fit_score)

    # Risk Score Calculation (0 = Safe, 100 = Maximum Risk)
    risk_score = 0
    if balls < 100: risk_score += 30
    elif balls < 200: risk_score += 15
    if matches < 15: risk_score += 20
    if ipl_balls == 0: risk_score += 25
    if consistency < 65: risk_score += 15
    if cat and cat.lower() == 'batter' and delta < 0: risk_score += 20
    if cat and cat.lower() == 'bowler' and delta > 0.5: risk_score += 20
    risk_score = min(98, max(5, risk_score))

    r_out = dict(r)
    # Ensure category key is clean
    if '\ufeffcategory' in r_out:
        r_out['category'] = r_out.pop('\ufeffcategory')
    r_out['country'] = country
    r_out['is_overseas'] = 'Yes' if is_overseas else 'No'
    r_out['skill_specialization'] = skill
    r_out['batting_style'] = bat_style
    r_out['bowling_style'] = bowl_style
    r_out['estimated_price_cr'] = price
    r_out['rr_tactical_fit'] = fit_score
    r_out['rr_role_target'] = role_fit
    r_out['phase_specialization'] = phase
    r_out['auction_tier'] = auction_tier
    r_out['risk_score'] = risk_score
    r_out['radar_output'] = r_output
    r_out['radar_delta'] = r_delta
    r_out['radar_sample'] = r_sample
    r_out['radar_consistency'] = r_consistency
    r_out['radar_ipl'] = r_ipl
    r_out['radar_synergy'] = r_synergy
    r_out['scout_verdict'] = verdict

    enriched_rows.append(r_out)

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(enriched_rows[0].keys()))
    writer.writeheader()
    writer.writerows(enriched_rows)

print(f'Successfully wrote {len(enriched_rows)} enriched player records to {output_file}!')

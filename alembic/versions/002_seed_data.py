"""seed world cup 2026 data

Revision ID: 002
Revises: 001
Create Date: 2026-04-07
"""
from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    # Admin user
    op.execute("""
        INSERT INTO users (email, password_hash, username, is_admin)
        VALUES ('admin@grandt.com', '$2b$12$ITsoUoc5W7t7BPHp6vtlT.o5WJAXkuwBMHBw2a7bMrHVqyBGM4iFC', 'admin', true)
    """)

    # Update existing test user to be admin
    op.execute("UPDATE users SET is_admin = true WHERE id = 1")

    # Match days
    op.execute("""
        INSERT INTO match_days (name, deadline) VALUES
        ('Fase de Grupos - Fecha 1', '2026-06-11 12:00:00'),
        ('Fase de Grupos - Fecha 2', '2026-06-15 12:00:00'),
        ('Fase de Grupos - Fecha 3', '2026-06-19 12:00:00'),
        ('Octavos de Final', '2026-06-23 12:00:00'),
        ('Cuartos de Final', '2026-06-27 12:00:00'),
        ('Semifinales', '2026-07-01 12:00:00'),
        ('Final', '2026-07-05 12:00:00')
    """)

    # Players - Argentina
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Emiliano Martínez', 'Argentina', 'arquero'),
        ('Franco Armani', 'Argentina', 'arquero'),
        ('Gerónimo Rulli', 'Argentina', 'arquero'),
        ('Nahuel Molina', 'Argentina', 'defensor'),
        ('Gonzalo Montiel', 'Argentina', 'defensor'),
        ('Cristian Romero', 'Argentina', 'defensor'),
        ('Nicolás Otamendi', 'Argentina', 'defensor'),
        ('Lisandro Martínez', 'Argentina', 'defensor'),
        ('Marcos Acuña', 'Argentina', 'defensor'),
        ('Nicolás Tagliafico', 'Argentina', 'defensor'),
        ('Rodrigo De Paul', 'Argentina', 'mediocampista'),
        ('Leandro Paredes', 'Argentina', 'mediocampista'),
        ('Alexis Mac Allister', 'Argentina', 'mediocampista'),
        ('Enzo Fernández', 'Argentina', 'mediocampista'),
        ('Giovani Lo Celso', 'Argentina', 'mediocampista'),
        ('Exequiel Palacios', 'Argentina', 'mediocampista'),
        ('Lionel Messi', 'Argentina', 'delantero'),
        ('Julián Álvarez', 'Argentina', 'delantero'),
        ('Lautaro Martínez', 'Argentina', 'delantero'),
        ('Ángel Di María', 'Argentina', 'delantero'),
        ('Paulo Dybala', 'Argentina', 'delantero'),
        ('Alejandro Garnacho', 'Argentina', 'delantero'),
        ('Thiago Almada', 'Argentina', 'mediocampista')
    """)

    # Players - Brasil
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Alisson Becker', 'Brasil', 'arquero'),
        ('Ederson Moraes', 'Brasil', 'arquero'),
        ('Weverton', 'Brasil', 'arquero'),
        ('Marquinhos', 'Brasil', 'defensor'),
        ('Éder Militão', 'Brasil', 'defensor'),
        ('Gabriel Magalhães', 'Brasil', 'defensor'),
        ('Danilo', 'Brasil', 'defensor'),
        ('Wendell', 'Brasil', 'defensor'),
        ('Bremer', 'Brasil', 'defensor'),
        ('Guilherme Arana', 'Brasil', 'defensor'),
        ('Casemiro', 'Brasil', 'mediocampista'),
        ('Lucas Paquetá', 'Brasil', 'mediocampista'),
        ('Bruno Guimarães', 'Brasil', 'mediocampista'),
        ('André', 'Brasil', 'mediocampista'),
        ('Gerson', 'Brasil', 'mediocampista'),
        ('João Gomes', 'Brasil', 'mediocampista'),
        ('Vinícius Jr.', 'Brasil', 'delantero'),
        ('Rodrygo', 'Brasil', 'delantero'),
        ('Raphinha', 'Brasil', 'delantero'),
        ('Endrick', 'Brasil', 'delantero'),
        ('Gabriel Martinelli', 'Brasil', 'delantero'),
        ('Richarlison', 'Brasil', 'delantero'),
        ('Savinho', 'Brasil', 'mediocampista')
    """)

    # Players - Francia
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Mike Maignan', 'Francia', 'arquero'),
        ('Alphonse Areola', 'Francia', 'arquero'),
        ('Brice Samba', 'Francia', 'arquero'),
        ('Theo Hernández', 'Francia', 'defensor'),
        ('Jules Koundé', 'Francia', 'defensor'),
        ('Dayot Upamecano', 'Francia', 'defensor'),
        ('William Saliba', 'Francia', 'defensor'),
        ('Ibrahima Konaté', 'Francia', 'defensor'),
        ('Benjamin Pavard', 'Francia', 'defensor'),
        ('Ferland Mendy', 'Francia', 'defensor'),
        ('Aurélien Tchouaméni', 'Francia', 'mediocampista'),
        ('N''Golo Kanté', 'Francia', 'mediocampista'),
        ('Eduardo Camavinga', 'Francia', 'mediocampista'),
        ('Adrien Rabiot', 'Francia', 'mediocampista'),
        ('Youssouf Fofana', 'Francia', 'mediocampista'),
        ('Warren Zaïre-Emery', 'Francia', 'mediocampista'),
        ('Kylian Mbappé', 'Francia', 'delantero'),
        ('Antoine Griezmann', 'Francia', 'delantero'),
        ('Ousmane Dembélé', 'Francia', 'delantero'),
        ('Marcus Thuram', 'Francia', 'delantero'),
        ('Randal Kolo Muani', 'Francia', 'delantero'),
        ('Olivier Giroud', 'Francia', 'delantero'),
        ('Michael Olise', 'Francia', 'mediocampista')
    """)

    # Players - Alemania
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Manuel Neuer', 'Alemania', 'arquero'),
        ('Marc-André ter Stegen', 'Alemania', 'arquero'),
        ('Oliver Baumann', 'Alemania', 'arquero'),
        ('Antonio Rüdiger', 'Alemania', 'defensor'),
        ('Jonathan Tah', 'Alemania', 'defensor'),
        ('Nico Schlotterbeck', 'Alemania', 'defensor'),
        ('David Raum', 'Alemania', 'defensor'),
        ('Benjamin Henrichs', 'Alemania', 'defensor'),
        ('Joshua Kimmich', 'Alemania', 'defensor'),
        ('Robin Koch', 'Alemania', 'defensor'),
        ('İlkay Gündoğan', 'Alemania', 'mediocampista'),
        ('Toni Kroos', 'Alemania', 'mediocampista'),
        ('Jamal Musiala', 'Alemania', 'mediocampista'),
        ('Florian Wirtz', 'Alemania', 'mediocampista'),
        ('Leon Goretzka', 'Alemania', 'mediocampista'),
        ('Robert Andrich', 'Alemania', 'mediocampista'),
        ('Leroy Sané', 'Alemania', 'delantero'),
        ('Kai Havertz', 'Alemania', 'delantero'),
        ('Serge Gnabry', 'Alemania', 'delantero'),
        ('Niclas Füllkrug', 'Alemania', 'delantero'),
        ('Deniz Undav', 'Alemania', 'delantero'),
        ('Chris Führich', 'Alemania', 'mediocampista'),
        ('Maximilian Beier', 'Alemania', 'delantero')
    """)

    # Players - España
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Unai Simón', 'España', 'arquero'),
        ('David Raya', 'España', 'arquero'),
        ('Robert Sánchez', 'España', 'arquero'),
        ('Dani Carvajal', 'España', 'defensor'),
        ('Aymeric Laporte', 'España', 'defensor'),
        ('Robin Le Normand', 'España', 'defensor'),
        ('Marc Cucurella', 'España', 'defensor'),
        ('Alejandro Grimaldo', 'España', 'defensor'),
        ('Pau Cubarsí', 'España', 'defensor'),
        ('Jesús Navas', 'España', 'defensor'),
        ('Rodri', 'España', 'mediocampista'),
        ('Pedri', 'España', 'mediocampista'),
        ('Gavi', 'España', 'mediocampista'),
        ('Fabián Ruiz', 'España', 'mediocampista'),
        ('Dani Olmo', 'España', 'mediocampista'),
        ('Mikel Merino', 'España', 'mediocampista'),
        ('Lamine Yamal', 'España', 'delantero'),
        ('Álvaro Morata', 'España', 'delantero'),
        ('Nico Williams', 'España', 'delantero'),
        ('Ferran Torres', 'España', 'delantero'),
        ('Mikel Oyarzabal', 'España', 'delantero'),
        ('Joselu', 'España', 'delantero'),
        ('Fermín López', 'España', 'mediocampista')
    """)

    # Players - Inglaterra
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Jordan Pickford', 'Inglaterra', 'arquero'),
        ('Aaron Ramsdale', 'Inglaterra', 'arquero'),
        ('Dean Henderson', 'Inglaterra', 'arquero'),
        ('Kyle Walker', 'Inglaterra', 'defensor'),
        ('John Stones', 'Inglaterra', 'defensor'),
        ('Harry Maguire', 'Inglaterra', 'defensor'),
        ('Luke Shaw', 'Inglaterra', 'defensor'),
        ('Trent Alexander-Arnold', 'Inglaterra', 'defensor'),
        ('Marc Guéhi', 'Inglaterra', 'defensor'),
        ('Ezri Konsa', 'Inglaterra', 'defensor'),
        ('Declan Rice', 'Inglaterra', 'mediocampista'),
        ('Jude Bellingham', 'Inglaterra', 'mediocampista'),
        ('Phil Foden', 'Inglaterra', 'mediocampista'),
        ('Kobbie Mainoo', 'Inglaterra', 'mediocampista'),
        ('Conor Gallagher', 'Inglaterra', 'mediocampista'),
        ('Adam Wharton', 'Inglaterra', 'mediocampista'),
        ('Harry Kane', 'Inglaterra', 'delantero'),
        ('Bukayo Saka', 'Inglaterra', 'delantero'),
        ('Marcus Rashford', 'Inglaterra', 'delantero'),
        ('Cole Palmer', 'Inglaterra', 'delantero'),
        ('Jarrod Bowen', 'Inglaterra', 'delantero'),
        ('Ollie Watkins', 'Inglaterra', 'delantero'),
        ('Anthony Gordon', 'Inglaterra', 'mediocampista')
    """)

    # Players - Portugal
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Diogo Costa', 'Portugal', 'arquero'),
        ('Rui Patrício', 'Portugal', 'arquero'),
        ('José Sá', 'Portugal', 'arquero'),
        ('Rúben Dias', 'Portugal', 'defensor'),
        ('Pepe', 'Portugal', 'defensor'),
        ('João Cancelo', 'Portugal', 'defensor'),
        ('Nuno Mendes', 'Portugal', 'defensor'),
        ('Diogo Dalot', 'Portugal', 'defensor'),
        ('António Silva', 'Portugal', 'defensor'),
        ('Gonçalo Inácio', 'Portugal', 'defensor'),
        ('Bruno Fernandes', 'Portugal', 'mediocampista'),
        ('Bernardo Silva', 'Portugal', 'mediocampista'),
        ('Vitinha', 'Portugal', 'mediocampista'),
        ('João Palhinha', 'Portugal', 'mediocampista'),
        ('Rúben Neves', 'Portugal', 'mediocampista'),
        ('João Neves', 'Portugal', 'mediocampista'),
        ('Cristiano Ronaldo', 'Portugal', 'delantero'),
        ('Rafael Leão', 'Portugal', 'delantero'),
        ('Gonçalo Ramos', 'Portugal', 'delantero'),
        ('Diogo Jota', 'Portugal', 'delantero'),
        ('Pedro Neto', 'Portugal', 'delantero'),
        ('Francisco Conceição', 'Portugal', 'delantero'),
        ('Otávio', 'Portugal', 'mediocampista')
    """)

    # Players - Países Bajos
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Bart Verbruggen', 'Países Bajos', 'arquero'),
        ('Justin Bijlow', 'Países Bajos', 'arquero'),
        ('Mark Flekken', 'Países Bajos', 'arquero'),
        ('Virgil van Dijk', 'Países Bajos', 'defensor'),
        ('Nathan Aké', 'Países Bajos', 'defensor'),
        ('Jurriën Timber', 'Países Bajos', 'defensor'),
        ('Stefan de Vrij', 'Países Bajos', 'defensor'),
        ('Denzel Dumfries', 'Países Bajos', 'defensor'),
        ('Matthijs de Ligt', 'Países Bajos', 'defensor'),
        ('Micky van de Ven', 'Países Bajos', 'defensor'),
        ('Frenkie de Jong', 'Países Bajos', 'mediocampista'),
        ('Teun Koopmeiners', 'Países Bajos', 'mediocampista'),
        ('Ryan Gravenberch', 'Países Bajos', 'mediocampista'),
        ('Jerdy Schouten', 'Países Bajos', 'mediocampista'),
        ('Xavi Simons', 'Países Bajos', 'mediocampista'),
        ('Tijjani Reijnders', 'Países Bajos', 'mediocampista'),
        ('Memphis Depay', 'Países Bajos', 'delantero'),
        ('Cody Gakpo', 'Países Bajos', 'delantero'),
        ('Donyell Malen', 'Países Bajos', 'delantero'),
        ('Steven Bergwijn', 'Países Bajos', 'delantero'),
        ('Wout Weghorst', 'Países Bajos', 'delantero'),
        ('Brian Brobbey', 'Países Bajos', 'delantero'),
        ('Joey Veerman', 'Países Bajos', 'mediocampista')
    """)

    # Players - Bélgica
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Thibaut Courtois', 'Bélgica', 'arquero'),
        ('Koen Casteels', 'Bélgica', 'arquero'),
        ('Matz Sels', 'Bélgica', 'arquero'),
        ('Jan Vertonghen', 'Bélgica', 'defensor'),
        ('Timothy Castagne', 'Bélgica', 'defensor'),
        ('Arthur Theate', 'Bélgica', 'defensor'),
        ('Wout Faes', 'Bélgica', 'defensor'),
        ('Zeno Debast', 'Bélgica', 'defensor'),
        ('Thomas Meunier', 'Bélgica', 'defensor'),
        ('Maxim De Cuyper', 'Bélgica', 'defensor'),
        ('Kevin De Bruyne', 'Bélgica', 'mediocampista'),
        ('Youri Tielemans', 'Bélgica', 'mediocampista'),
        ('Amadou Onana', 'Bélgica', 'mediocampista'),
        ('Orel Mangala', 'Bélgica', 'mediocampista'),
        ('Aster Vranckx', 'Bélgica', 'mediocampista'),
        ('Charles De Ketelaere', 'Bélgica', 'mediocampista'),
        ('Romelu Lukaku', 'Bélgica', 'delantero'),
        ('Jérémy Doku', 'Bélgica', 'delantero'),
        ('Leandro Trossard', 'Bélgica', 'delantero'),
        ('Loïs Openda', 'Bélgica', 'delantero'),
        ('Johan Bakayoko', 'Bélgica', 'delantero'),
        ('Dodi Lukebakio', 'Bélgica', 'delantero'),
        ('Yannick Carrasco', 'Bélgica', 'mediocampista')
    """)

    # Players - Italia
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Gianluigi Donnarumma', 'Italia', 'arquero'),
        ('Alex Meret', 'Italia', 'arquero'),
        ('Guglielmo Vicario', 'Italia', 'arquero'),
        ('Alessandro Bastoni', 'Italia', 'defensor'),
        ('Riccardo Calafiori', 'Italia', 'defensor'),
        ('Federico Dimarco', 'Italia', 'defensor'),
        ('Giovanni Di Lorenzo', 'Italia', 'defensor'),
        ('Andrea Cambiaso', 'Italia', 'defensor'),
        ('Gianluca Mancini', 'Italia', 'defensor'),
        ('Matteo Darmian', 'Italia', 'defensor'),
        ('Nicolò Barella', 'Italia', 'mediocampista'),
        ('Sandro Tonali', 'Italia', 'mediocampista'),
        ('Jorginho', 'Italia', 'mediocampista'),
        ('Lorenzo Pellegrini', 'Italia', 'mediocampista'),
        ('Davide Frattesi', 'Italia', 'mediocampista'),
        ('Samuele Ricci', 'Italia', 'mediocampista'),
        ('Federico Chiesa', 'Italia', 'delantero'),
        ('Gianluca Scamacca', 'Italia', 'delantero'),
        ('Mateo Retegui', 'Italia', 'delantero'),
        ('Giacomo Raspadori', 'Italia', 'delantero'),
        ('Stephan El Shaarawy', 'Italia', 'delantero'),
        ('Mattia Zaccagni', 'Italia', 'delantero'),
        ('Bryan Cristante', 'Italia', 'mediocampista')
    """)

    # Players - Uruguay
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Sergio Rochet', 'Uruguay', 'arquero'),
        ('Fernando Muslera', 'Uruguay', 'arquero'),
        ('Santiago Mele', 'Uruguay', 'arquero'),
        ('José María Giménez', 'Uruguay', 'defensor'),
        ('Ronald Araújo', 'Uruguay', 'defensor'),
        ('Sebastián Coates', 'Uruguay', 'defensor'),
        ('Mathías Olivera', 'Uruguay', 'defensor'),
        ('Nahitan Nández', 'Uruguay', 'defensor'),
        ('Guillermo Varela', 'Uruguay', 'defensor'),
        ('Matías Viña', 'Uruguay', 'defensor'),
        ('Federico Valverde', 'Uruguay', 'mediocampista'),
        ('Rodrigo Bentancur', 'Uruguay', 'mediocampista'),
        ('Manuel Ugarte', 'Uruguay', 'mediocampista'),
        ('Nicolás de la Cruz', 'Uruguay', 'mediocampista'),
        ('Giorgian De Arrascaeta', 'Uruguay', 'mediocampista'),
        ('Facundo Pellistri', 'Uruguay', 'mediocampista'),
        ('Darwin Núñez', 'Uruguay', 'delantero'),
        ('Luis Suárez', 'Uruguay', 'delantero'),
        ('Maximiliano Gómez', 'Uruguay', 'delantero'),
        ('Agustín Canobbio', 'Uruguay', 'delantero'),
        ('Cristian Olivera', 'Uruguay', 'delantero'),
        ('Brian Rodríguez', 'Uruguay', 'delantero'),
        ('Agustín Álvarez Martínez', 'Uruguay', 'mediocampista')
    """)

    # Players - Colombia
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('David Ospina', 'Colombia', 'arquero'),
        ('Camilo Vargas', 'Colombia', 'arquero'),
        ('Álvaro Montero', 'Colombia', 'arquero'),
        ('Davinson Sánchez', 'Colombia', 'defensor'),
        ('Yerry Mina', 'Colombia', 'defensor'),
        ('Carlos Cuesta', 'Colombia', 'defensor'),
        ('Johan Mojica', 'Colombia', 'defensor'),
        ('Daniel Muñoz', 'Colombia', 'defensor'),
        ('Santiago Arias', 'Colombia', 'defensor'),
        ('Jhon Lucumí', 'Colombia', 'defensor'),
        ('James Rodríguez', 'Colombia', 'mediocampista'),
        ('Juan Quintero', 'Colombia', 'mediocampista'),
        ('Mateus Uribe', 'Colombia', 'mediocampista'),
        ('Jefferson Lerma', 'Colombia', 'mediocampista'),
        ('Richard Ríos', 'Colombia', 'mediocampista'),
        ('Jhon Arias', 'Colombia', 'mediocampista'),
        ('Luis Díaz', 'Colombia', 'delantero'),
        ('Rafael Santos Borré', 'Colombia', 'delantero'),
        ('Jhon Córdoba', 'Colombia', 'delantero'),
        ('Miguel Borja', 'Colombia', 'delantero'),
        ('Luis Sinisterra', 'Colombia', 'delantero'),
        ('Jhon Durán', 'Colombia', 'delantero'),
        ('Jorge Carrascal', 'Colombia', 'mediocampista')
    """)

    # Players - México
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Guillermo Ochoa', 'México', 'arquero'),
        ('Luis Malagón', 'México', 'arquero'),
        ('Carlos Acevedo', 'México', 'arquero'),
        ('César Montes', 'México', 'defensor'),
        ('Jorge Sánchez', 'México', 'defensor'),
        ('Johan Vásquez', 'México', 'defensor'),
        ('Jesús Gallardo', 'México', 'defensor'),
        ('Gerardo Arteaga', 'México', 'defensor'),
        ('Julián Araujo', 'México', 'defensor'),
        ('Kevin Álvarez', 'México', 'defensor'),
        ('Edson Álvarez', 'México', 'mediocampista'),
        ('Héctor Herrera', 'México', 'mediocampista'),
        ('Luis Romo', 'México', 'mediocampista'),
        ('Orbelín Pineda', 'México', 'mediocampista'),
        ('Carlos Rodríguez', 'México', 'mediocampista'),
        ('Diego Lainez', 'México', 'mediocampista'),
        ('Hirving Lozano', 'México', 'delantero'),
        ('Raúl Jiménez', 'México', 'delantero'),
        ('Henry Martín', 'México', 'delantero'),
        ('Santiago Giménez', 'México', 'delantero'),
        ('Alexis Vega', 'México', 'delantero'),
        ('Roberto Alvarado', 'México', 'delantero'),
        ('Uriel Antuna', 'México', 'mediocampista')
    """)

    # Players - Estados Unidos
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Matt Turner', 'Estados Unidos', 'arquero'),
        ('Ethan Horvath', 'Estados Unidos', 'arquero'),
        ('Sean Johnson', 'Estados Unidos', 'arquero'),
        ('Sergiño Dest', 'Estados Unidos', 'defensor'),
        ('Antonee Robinson', 'Estados Unidos', 'defensor'),
        ('Chris Richards', 'Estados Unidos', 'defensor'),
        ('Tim Ream', 'Estados Unidos', 'defensor'),
        ('Miles Robinson', 'Estados Unidos', 'defensor'),
        ('Joe Scally', 'Estados Unidos', 'defensor'),
        ('Mark McKenzie', 'Estados Unidos', 'defensor'),
        ('Tyler Adams', 'Estados Unidos', 'mediocampista'),
        ('Weston McKennie', 'Estados Unidos', 'mediocampista'),
        ('Yunus Musah', 'Estados Unidos', 'mediocampista'),
        ('Gio Reyna', 'Estados Unidos', 'mediocampista'),
        ('Brenden Aaronson', 'Estados Unidos', 'mediocampista'),
        ('Johnny Cardoso', 'Estados Unidos', 'mediocampista'),
        ('Christian Pulisic', 'Estados Unidos', 'delantero'),
        ('Timothy Weah', 'Estados Unidos', 'delantero'),
        ('Josh Sargent', 'Estados Unidos', 'delantero'),
        ('Folarin Balogun', 'Estados Unidos', 'delantero'),
        ('Ricardo Pepi', 'Estados Unidos', 'delantero'),
        ('Haji Wright', 'Estados Unidos', 'delantero'),
        ('Luca de la Torre', 'Estados Unidos', 'mediocampista')
    """)

    # Players - Canadá
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Milan Borjan', 'Canadá', 'arquero'),
        ('Maxime Crépeau', 'Canadá', 'arquero'),
        ('Dayne St. Clair', 'Canadá', 'arquero'),
        ('Alphonso Davies', 'Canadá', 'defensor'),
        ('Alistair Johnston', 'Canadá', 'defensor'),
        ('Kamal Miller', 'Canadá', 'defensor'),
        ('Steven Vitória', 'Canadá', 'defensor'),
        ('Richie Laryea', 'Canadá', 'defensor'),
        ('Derek Cornelius', 'Canadá', 'defensor'),
        ('Moise Bombito', 'Canadá', 'defensor'),
        ('Stephen Eustáquio', 'Canadá', 'mediocampista'),
        ('Jonathan Osorio', 'Canadá', 'mediocampista'),
        ('Ismaël Koné', 'Canadá', 'mediocampista'),
        ('Mark-Anthony Kaye', 'Canadá', 'mediocampista'),
        ('Samuel Piette', 'Canadá', 'mediocampista'),
        ('Liam Millar', 'Canadá', 'mediocampista'),
        ('Jonathan David', 'Canadá', 'delantero'),
        ('Cyle Larin', 'Canadá', 'delantero'),
        ('Tajon Buchanan', 'Canadá', 'delantero'),
        ('Junior Hoilett', 'Canadá', 'delantero'),
        ('Theo Corbeanu', 'Canadá', 'delantero'),
        ('Iké Ugbo', 'Canadá', 'delantero'),
        ('Ali Ahmed', 'Canadá', 'mediocampista')
    """)

    # Players - Japón
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Shūichi Gonda', 'Japón', 'arquero'),
        ('Daniel Schmidt', 'Japón', 'arquero'),
        ('Zion Suzuki', 'Japón', 'arquero'),
        ('Takehiro Tomiyasu', 'Japón', 'defensor'),
        ('Ko Itakura', 'Japón', 'defensor'),
        ('Shogo Taniguchi', 'Japón', 'defensor'),
        ('Hiroki Ito', 'Japón', 'defensor'),
        ('Yuto Nagatomo', 'Japón', 'defensor'),
        ('Miki Yamane', 'Japón', 'defensor'),
        ('Hiroki Sakai', 'Japón', 'defensor'),
        ('Wataru Endo', 'Japón', 'mediocampista'),
        ('Takefusa Kubo', 'Japón', 'mediocampista'),
        ('Kaoru Mitoma', 'Japón', 'mediocampista'),
        ('Daichi Kamada', 'Japón', 'mediocampista'),
        ('Hidemasa Morita', 'Japón', 'mediocampista'),
        ('Ao Tanaka', 'Japón', 'mediocampista'),
        ('Takumi Minamino', 'Japón', 'delantero'),
        ('Daizen Maeda', 'Japón', 'delantero'),
        ('Ayase Ueda', 'Japón', 'delantero'),
        ('Kyogo Furuhashi', 'Japón', 'delantero'),
        ('Ritsu Doan', 'Japón', 'delantero'),
        ('Junya Ito', 'Japón', 'delantero'),
        ('Keito Nakamura', 'Japón', 'mediocampista')
    """)

    # Players - Corea del Sur
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Kim Seung-gyu', 'Corea del Sur', 'arquero'),
        ('Jo Hyeon-woo', 'Corea del Sur', 'arquero'),
        ('Song Bum-keun', 'Corea del Sur', 'arquero'),
        ('Kim Min-jae', 'Corea del Sur', 'defensor'),
        ('Kim Young-gwon', 'Corea del Sur', 'defensor'),
        ('Kim Jin-su', 'Corea del Sur', 'defensor'),
        ('Hong Chul', 'Corea del Sur', 'defensor'),
        ('Yoon Jong-gyu', 'Corea del Sur', 'defensor'),
        ('Cho Yu-min', 'Corea del Sur', 'defensor'),
        ('Park Ji-su', 'Corea del Sur', 'defensor'),
        ('Son Heung-min', 'Corea del Sur', 'mediocampista'),
        ('Lee Jae-sung', 'Corea del Sur', 'mediocampista'),
        ('Hwang In-beom', 'Corea del Sur', 'mediocampista'),
        ('Jung Woo-young', 'Corea del Sur', 'mediocampista'),
        ('Lee Kang-in', 'Corea del Sur', 'mediocampista'),
        ('Paik Seung-ho', 'Corea del Sur', 'mediocampista'),
        ('Hwang Hee-chan', 'Corea del Sur', 'delantero'),
        ('Cho Gue-sung', 'Corea del Sur', 'delantero'),
        ('Song Min-kyu', 'Corea del Sur', 'delantero'),
        ('Oh Hyeon-gyu', 'Corea del Sur', 'delantero'),
        ('Na Sang-ho', 'Corea del Sur', 'delantero'),
        ('Jeong Sang-bin', 'Corea del Sur', 'delantero'),
        ('Kwon Chang-hoon', 'Corea del Sur', 'mediocampista')
    """)

    # Players - Australia
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Mathew Ryan', 'Australia', 'arquero'),
        ('Andrew Redmayne', 'Australia', 'arquero'),
        ('Joe Gauci', 'Australia', 'arquero'),
        ('Aziz Behich', 'Australia', 'defensor'),
        ('Harry Souttar', 'Australia', 'defensor'),
        ('Kye Rowles', 'Australia', 'defensor'),
        ('Nathaniel Atkinson', 'Australia', 'defensor'),
        ('Miloš Degenek', 'Australia', 'defensor'),
        ('Joel King', 'Australia', 'defensor'),
        ('Thomas Deng', 'Australia', 'defensor'),
        ('Aaron Mooy', 'Australia', 'mediocampista'),
        ('Jackson Irvine', 'Australia', 'mediocampista'),
        ('Ajdin Hrustić', 'Australia', 'mediocampista'),
        ('Riley McGree', 'Australia', 'mediocampista'),
        ('Connor Metcalfe', 'Australia', 'mediocampista'),
        ('Cameron Devlin', 'Australia', 'mediocampista'),
        ('Mathew Leckie', 'Australia', 'delantero'),
        ('Mitchell Duke', 'Australia', 'delantero'),
        ('Jamie Maclaren', 'Australia', 'delantero'),
        ('Martin Boyle', 'Australia', 'delantero'),
        ('Awer Mabil', 'Australia', 'delantero'),
        ('Garang Kuol', 'Australia', 'delantero'),
        ('Keanu Baccus', 'Australia', 'mediocampista')
    """)

    # Players - Marruecos
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Yassine Bounou', 'Marruecos', 'arquero'),
        ('Munir El Kajoui', 'Marruecos', 'arquero'),
        ('Ahmed Reda Tagnaouti', 'Marruecos', 'arquero'),
        ('Achraf Hakimi', 'Marruecos', 'defensor'),
        ('Noussair Mazraoui', 'Marruecos', 'defensor'),
        ('Nayef Aguerd', 'Marruecos', 'defensor'),
        ('Romain Saïss', 'Marruecos', 'defensor'),
        ('Jawad El Yamiq', 'Marruecos', 'defensor'),
        ('Adam Masina', 'Marruecos', 'defensor'),
        ('Achraf Dari', 'Marruecos', 'defensor'),
        ('Sofyan Amrabat', 'Marruecos', 'mediocampista'),
        ('Azzedine Ounahi', 'Marruecos', 'mediocampista'),
        ('Bilal El Khannouss', 'Marruecos', 'mediocampista'),
        ('Selim Amallah', 'Marruecos', 'mediocampista'),
        ('Sofiane Boufal', 'Marruecos', 'mediocampista'),
        ('Ilias Chair', 'Marruecos', 'mediocampista'),
        ('Hakim Ziyech', 'Marruecos', 'delantero'),
        ('Youssef En-Nesyri', 'Marruecos', 'delantero'),
        ('Sofiane Rahimi', 'Marruecos', 'delantero'),
        ('Abde Ezzalzouli', 'Marruecos', 'delantero'),
        ('Ayoub El Kaabi', 'Marruecos', 'delantero'),
        ('Brahim Díaz', 'Marruecos', 'delantero'),
        ('Amine Harit', 'Marruecos', 'mediocampista')
    """)

    # Players - Senegal
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Édouard Mendy', 'Senegal', 'arquero'),
        ('Alfred Gomis', 'Senegal', 'arquero'),
        ('Seny Dieng', 'Senegal', 'arquero'),
        ('Kalidou Koulibaly', 'Senegal', 'defensor'),
        ('Abdou Diallo', 'Senegal', 'defensor'),
        ('Youssouf Sabaly', 'Senegal', 'defensor'),
        ('Formose Mendy', 'Senegal', 'defensor'),
        ('Ismail Jakobs', 'Senegal', 'defensor'),
        ('Pape Abou Cissé', 'Senegal', 'defensor'),
        ('Moussa Niakhaté', 'Senegal', 'defensor'),
        ('Idrissa Gueye', 'Senegal', 'mediocampista'),
        ('Cheikhou Kouyaté', 'Senegal', 'mediocampista'),
        ('Nampalys Mendy', 'Senegal', 'mediocampista'),
        ('Pape Matar Sarr', 'Senegal', 'mediocampista'),
        ('Pathé Ciss', 'Senegal', 'mediocampista'),
        ('Lamine Camara', 'Senegal', 'mediocampista'),
        ('Sadio Mané', 'Senegal', 'delantero'),
        ('Ismaïla Sarr', 'Senegal', 'delantero'),
        ('Boulaye Dia', 'Senegal', 'delantero'),
        ('Famara Diédhiou', 'Senegal', 'delantero'),
        ('Nicolas Jackson', 'Senegal', 'delantero'),
        ('Iliman Ndiaye', 'Senegal', 'delantero'),
        ('Habib Diarra', 'Senegal', 'mediocampista')
    """)

    # Players - Nigeria
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Francis Uzoho', 'Nigeria', 'arquero'),
        ('Maduka Okoye', 'Nigeria', 'arquero'),
        ('Stanley Nwabali', 'Nigeria', 'arquero'),
        ('William Ekong', 'Nigeria', 'defensor'),
        ('Calvin Bassey', 'Nigeria', 'defensor'),
        ('Ola Aina', 'Nigeria', 'defensor'),
        ('Semi Ajayi', 'Nigeria', 'defensor'),
        ('Bright Osayi-Samuel', 'Nigeria', 'defensor'),
        ('Olaoluwa Aina', 'Nigeria', 'defensor'),
        ('Zaidu Sanusi', 'Nigeria', 'defensor'),
        ('Wilfred Ndidi', 'Nigeria', 'mediocampista'),
        ('Alex Iwobi', 'Nigeria', 'mediocampista'),
        ('Joe Aribo', 'Nigeria', 'mediocampista'),
        ('Raphael Onyedika', 'Nigeria', 'mediocampista'),
        ('Frank Onyeka', 'Nigeria', 'mediocampista'),
        ('Fisayo Dele-Bashiru', 'Nigeria', 'mediocampista'),
        ('Victor Osimhen', 'Nigeria', 'delantero'),
        ('Samuel Chukwueze', 'Nigeria', 'delantero'),
        ('Ademola Lookman', 'Nigeria', 'delantero'),
        ('Kelechi Iheanacho', 'Nigeria', 'delantero'),
        ('Moses Simon', 'Nigeria', 'delantero'),
        ('Paul Onuachu', 'Nigeria', 'delantero'),
        ('Taiwo Awoniyi', 'Nigeria', 'mediocampista')
    """)

    # Players - Ecuador
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Hernán Galíndez', 'Ecuador', 'arquero'),
        ('Alexander Domínguez', 'Ecuador', 'arquero'),
        ('Moisés Ramírez', 'Ecuador', 'arquero'),
        ('Piero Hincapié', 'Ecuador', 'defensor'),
        ('Robert Arboleda', 'Ecuador', 'defensor'),
        ('Félix Torres', 'Ecuador', 'defensor'),
        ('Pervis Estupiñán', 'Ecuador', 'defensor'),
        ('Angelo Preciado', 'Ecuador', 'defensor'),
        ('Xavier Arreaga', 'Ecuador', 'defensor'),
        ('Diego Palacios', 'Ecuador', 'defensor'),
        ('Moisés Caicedo', 'Ecuador', 'mediocampista'),
        ('Carlos Gruezo', 'Ecuador', 'mediocampista'),
        ('Jhegson Méndez', 'Ecuador', 'mediocampista'),
        ('Alan Franco', 'Ecuador', 'mediocampista'),
        ('Jeremy Sarmiento', 'Ecuador', 'mediocampista'),
        ('Gonzalo Plata', 'Ecuador', 'mediocampista'),
        ('Enner Valencia', 'Ecuador', 'delantero'),
        ('Michael Estrada', 'Ecuador', 'delantero'),
        ('Kevin Rodríguez', 'Ecuador', 'delantero'),
        ('Jordy Caicedo', 'Ecuador', 'delantero'),
        ('Kendry Páez', 'Ecuador', 'delantero'),
        ('John Yeboah', 'Ecuador', 'delantero'),
        ('Ángel Mena', 'Ecuador', 'mediocampista')
    """)

    # Players - Croacia
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Dominik Livaković', 'Croacia', 'arquero'),
        ('Ivica Ivušić', 'Croacia', 'arquero'),
        ('Nediljko Labrović', 'Croacia', 'arquero'),
        ('Joško Gvardiol', 'Croacia', 'defensor'),
        ('Domagoj Vida', 'Croacia', 'defensor'),
        ('Dejan Lovren', 'Croacia', 'defensor'),
        ('Borna Sosa', 'Croacia', 'defensor'),
        ('Josip Stanišić', 'Croacia', 'defensor'),
        ('Duje Ćaleta-Car', 'Croacia', 'defensor'),
        ('Martin Erlić', 'Croacia', 'defensor'),
        ('Luka Modrić', 'Croacia', 'mediocampista'),
        ('Mateo Kovačić', 'Croacia', 'mediocampista'),
        ('Marcelo Brozović', 'Croacia', 'mediocampista'),
        ('Mario Pašalić', 'Croacia', 'mediocampista'),
        ('Lovro Majer', 'Croacia', 'mediocampista'),
        ('Luka Sučić', 'Croacia', 'mediocampista'),
        ('Ivan Perišić', 'Croacia', 'delantero'),
        ('Andrej Kramarić', 'Croacia', 'delantero'),
        ('Bruno Petković', 'Croacia', 'delantero'),
        ('Ante Budimir', 'Croacia', 'delantero'),
        ('Marko Livaja', 'Croacia', 'delantero'),
        ('Igor Matanović', 'Croacia', 'delantero'),
        ('Nikola Vlašić', 'Croacia', 'mediocampista')
    """)

    # Players - Dinamarca
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Kasper Schmeichel', 'Dinamarca', 'arquero'),
        ('Frederik Rønnow', 'Dinamarca', 'arquero'),
        ('Mads Hermansen', 'Dinamarca', 'arquero'),
        ('Simon Kjær', 'Dinamarca', 'defensor'),
        ('Andreas Christensen', 'Dinamarca', 'defensor'),
        ('Jannik Vestergaard', 'Dinamarca', 'defensor'),
        ('Joakim Mæhle', 'Dinamarca', 'defensor'),
        ('Victor Kristiansen', 'Dinamarca', 'defensor'),
        ('Alexander Bah', 'Dinamarca', 'defensor'),
        ('Joachim Andersen', 'Dinamarca', 'defensor'),
        ('Christian Eriksen', 'Dinamarca', 'mediocampista'),
        ('Pierre-Emile Højbjerg', 'Dinamarca', 'mediocampista'),
        ('Thomas Delaney', 'Dinamarca', 'mediocampista'),
        ('Morten Hjulmand', 'Dinamarca', 'mediocampista'),
        ('Mikkel Damsgaard', 'Dinamarca', 'mediocampista'),
        ('Matt O''Riley', 'Dinamarca', 'mediocampista'),
        ('Rasmus Højlund', 'Dinamarca', 'delantero'),
        ('Jonas Wind', 'Dinamarca', 'delantero'),
        ('Kasper Dolberg', 'Dinamarca', 'delantero'),
        ('Andreas Skov Olsen', 'Dinamarca', 'delantero'),
        ('Yussuf Poulsen', 'Dinamarca', 'delantero'),
        ('Jacob Bruun Larsen', 'Dinamarca', 'delantero'),
        ('Jesper Lindstrøm', 'Dinamarca', 'mediocampista')
    """)

    # Players - Suiza
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Yann Sommer', 'Suiza', 'arquero'),
        ('Gregor Kobel', 'Suiza', 'arquero'),
        ('Philipp Köhn', 'Suiza', 'arquero'),
        ('Manuel Akanji', 'Suiza', 'defensor'),
        ('Fabian Schär', 'Suiza', 'defensor'),
        ('Ricardo Rodríguez', 'Suiza', 'defensor'),
        ('Silvan Widmer', 'Suiza', 'defensor'),
        ('Nico Elvedi', 'Suiza', 'defensor'),
        ('Leonidas Stergiou', 'Suiza', 'defensor'),
        ('Ulisses Garcia', 'Suiza', 'defensor'),
        ('Granit Xhaka', 'Suiza', 'mediocampista'),
        ('Denis Zakaria', 'Suiza', 'mediocampista'),
        ('Remo Freuler', 'Suiza', 'mediocampista'),
        ('Djibril Sow', 'Suiza', 'mediocampista'),
        ('Michel Aebischer', 'Suiza', 'mediocampista'),
        ('Fabian Rieder', 'Suiza', 'mediocampista'),
        ('Xherdan Shaqiri', 'Suiza', 'delantero'),
        ('Breel Embolo', 'Suiza', 'delantero'),
        ('Noah Okafor', 'Suiza', 'delantero'),
        ('Ruben Vargas', 'Suiza', 'delantero'),
        ('Dan Ndoye', 'Suiza', 'delantero'),
        ('Zeki Amdouni', 'Suiza', 'delantero'),
        ('Vincent Sierro', 'Suiza', 'mediocampista')
    """)

    # Players - Polonia
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Wojciech Szczęsny', 'Polonia', 'arquero'),
        ('Łukasz Skorupski', 'Polonia', 'arquero'),
        ('Marcin Bułka', 'Polonia', 'arquero'),
        ('Jan Bednarek', 'Polonia', 'defensor'),
        ('Kamil Glik', 'Polonia', 'defensor'),
        ('Matty Cash', 'Polonia', 'defensor'),
        ('Bartosz Bereszyński', 'Polonia', 'defensor'),
        ('Jakub Kiwior', 'Polonia', 'defensor'),
        ('Paweł Dawidowicz', 'Polonia', 'defensor'),
        ('Nicola Zalewski', 'Polonia', 'defensor'),
        ('Piotr Zieliński', 'Polonia', 'mediocampista'),
        ('Grzegorz Krychowiak', 'Polonia', 'mediocampista'),
        ('Damian Szymański', 'Polonia', 'mediocampista'),
        ('Jakub Moder', 'Polonia', 'mediocampista'),
        ('Sebastian Szymański', 'Polonia', 'mediocampista'),
        ('Jakub Piotrowski', 'Polonia', 'mediocampista'),
        ('Robert Lewandowski', 'Polonia', 'delantero'),
        ('Arkadiusz Milik', 'Polonia', 'delantero'),
        ('Krzysztof Piątek', 'Polonia', 'delantero'),
        ('Karol Świderski', 'Polonia', 'delantero'),
        ('Adam Buksa', 'Polonia', 'delantero'),
        ('Kamil Grosicki', 'Polonia', 'delantero'),
        ('Przemysław Frankowski', 'Polonia', 'mediocampista')
    """)

    # Players - Serbia
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Predrag Rajković', 'Serbia', 'arquero'),
        ('Vanja Milinković-Savić', 'Serbia', 'arquero'),
        ('Đorđe Petrović', 'Serbia', 'arquero'),
        ('Nikola Milenković', 'Serbia', 'defensor'),
        ('Strahinja Pavlović', 'Serbia', 'defensor'),
        ('Miloš Veljković', 'Serbia', 'defensor'),
        ('Filip Mladenović', 'Serbia', 'defensor'),
        ('Srđan Babić', 'Serbia', 'defensor'),
        ('Strahinja Eraković', 'Serbia', 'defensor'),
        ('Nemanja Stojić', 'Serbia', 'defensor'),
        ('Sergej Milinković-Savić', 'Serbia', 'mediocampista'),
        ('Dušan Tadić', 'Serbia', 'mediocampista'),
        ('Nemanja Gudelj', 'Serbia', 'mediocampista'),
        ('Filip Kostić', 'Serbia', 'mediocampista'),
        ('Saša Lukić', 'Serbia', 'mediocampista'),
        ('Ivan Ilić', 'Serbia', 'mediocampista'),
        ('Dušan Vlahović', 'Serbia', 'delantero'),
        ('Aleksandar Mitrović', 'Serbia', 'delantero'),
        ('Luka Jović', 'Serbia', 'delantero'),
        ('Filip Đuričić', 'Serbia', 'delantero'),
        ('Andrija Živković', 'Serbia', 'delantero'),
        ('Nemanja Radonjić', 'Serbia', 'delantero'),
        ('Mijat Gaćinović', 'Serbia', 'mediocampista')
    """)

    # Players - Arabia Saudita
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Mohammed Al-Owais', 'Arabia Saudita', 'arquero'),
        ('Mohammed Al-Rubaie', 'Arabia Saudita', 'arquero'),
        ('Nawaf Al-Aqidi', 'Arabia Saudita', 'arquero'),
        ('Yasser Al-Shahrani', 'Arabia Saudita', 'defensor'),
        ('Ali Al-Boleahi', 'Arabia Saudita', 'defensor'),
        ('Abdulelah Al-Amri', 'Arabia Saudita', 'defensor'),
        ('Hassan Tambakti', 'Arabia Saudita', 'defensor'),
        ('Sultan Al-Ghannam', 'Arabia Saudita', 'defensor'),
        ('Saud Abdulhamid', 'Arabia Saudita', 'defensor'),
        ('Abdullah Madu', 'Arabia Saudita', 'defensor'),
        ('Salem Al-Dawsari', 'Arabia Saudita', 'mediocampista'),
        ('Mohamed Kanno', 'Arabia Saudita', 'mediocampista'),
        ('Abdulellah Al-Malki', 'Arabia Saudita', 'mediocampista'),
        ('Sami Al-Najei', 'Arabia Saudita', 'mediocampista'),
        ('Nasser Al-Dawsari', 'Arabia Saudita', 'mediocampista'),
        ('Abdullah Otayf', 'Arabia Saudita', 'mediocampista'),
        ('Firas Al-Buraikan', 'Arabia Saudita', 'delantero'),
        ('Saleh Al-Shehri', 'Arabia Saudita', 'delantero'),
        ('Abdullah Al-Hamdan', 'Arabia Saudita', 'delantero'),
        ('Haitham Asiri', 'Arabia Saudita', 'delantero'),
        ('Ayman Yahya', 'Arabia Saudita', 'delantero'),
        ('Abdulrahman Ghareeb', 'Arabia Saudita', 'delantero'),
        ('Ali Al-Hassan', 'Arabia Saudita', 'mediocampista')
    """)

    # Players - Ghana
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Richard Ofori', 'Ghana', 'arquero'),
        ('Lawrence Ati-Zigi', 'Ghana', 'arquero'),
        ('Ibrahim Danlad', 'Ghana', 'arquero'),
        ('Mohammed Salisu', 'Ghana', 'defensor'),
        ('Daniel Amartey', 'Ghana', 'defensor'),
        ('Alexander Djiku', 'Ghana', 'defensor'),
        ('Tariq Lamptey', 'Ghana', 'defensor'),
        ('Gideon Mensah', 'Ghana', 'defensor'),
        ('Denis Odoi', 'Ghana', 'defensor'),
        ('Alidu Seidu', 'Ghana', 'defensor'),
        ('Thomas Partey', 'Ghana', 'mediocampista'),
        ('Mohammed Kudus', 'Ghana', 'mediocampista'),
        ('André Ayew', 'Ghana', 'mediocampista'),
        ('Elisha Owusu', 'Ghana', 'mediocampista'),
        ('Salis Abdul Samed', 'Ghana', 'mediocampista'),
        ('Ibrahim Sulemana', 'Ghana', 'mediocampista'),
        ('Jordan Ayew', 'Ghana', 'delantero'),
        ('Inaki Williams', 'Ghana', 'delantero'),
        ('Antoine Semenyo', 'Ghana', 'delantero'),
        ('Osman Bukari', 'Ghana', 'delantero'),
        ('Ernest Nuamah', 'Ghana', 'delantero'),
        ('Fatawu Issahaku', 'Ghana', 'delantero'),
        ('Kamaldeen Sulemana', 'Ghana', 'mediocampista')
    """)

    # Players - Camerún
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('André Onana', 'Camerún', 'arquero'),
        ('Devis Epassy', 'Camerún', 'arquero'),
        ('Simon Ngapandouetnbu', 'Camerún', 'arquero'),
        ('Nicolas Nkoulou', 'Camerún', 'defensor'),
        ('Jean-Charles Castelletto', 'Camerún', 'defensor'),
        ('Christopher Wooh', 'Camerún', 'defensor'),
        ('Collins Fai', 'Camerún', 'defensor'),
        ('Nouhou Tolo', 'Camerún', 'defensor'),
        ('Olivier Mbaizo', 'Camerún', 'defensor'),
        ('Enzo Ebosse', 'Camerún', 'defensor'),
        ('André-Frank Zambo Anguissa', 'Camerún', 'mediocampista'),
        ('Martin Hongla', 'Camerún', 'mediocampista'),
        ('Pierre Kunde', 'Camerún', 'mediocampista'),
        ('Samuel Oum Gouet', 'Camerún', 'mediocampista'),
        ('Olivier Ntcham', 'Camerún', 'mediocampista'),
        ('Georges-Kévin Nkoudou', 'Camerún', 'mediocampista'),
        ('Vincent Aboubakar', 'Camerún', 'delantero'),
        ('Eric Maxim Choupo-Moting', 'Camerún', 'delantero'),
        ('Karl Toko Ekambi', 'Camerún', 'delantero'),
        ('Bryan Mbeumo', 'Camerún', 'delantero'),
        ('Christian Bassogog', 'Camerún', 'delantero'),
        ('Nicolas Moumi Ngamaleu', 'Camerún', 'delantero'),
        ('Jean Onana', 'Camerún', 'mediocampista')
    """)

    # Players - Chile
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Claudio Bravo', 'Chile', 'arquero'),
        ('Gabriel Arias', 'Chile', 'arquero'),
        ('Brayan Cortés', 'Chile', 'arquero'),
        ('Gary Medel', 'Chile', 'defensor'),
        ('Guillermo Maripán', 'Chile', 'defensor'),
        ('Paulo Díaz', 'Chile', 'defensor'),
        ('Gabriel Suazo', 'Chile', 'defensor'),
        ('Mauricio Isla', 'Chile', 'defensor'),
        ('Igor Lichnovsky', 'Chile', 'defensor'),
        ('Thomas Galdames', 'Chile', 'defensor'),
        ('Arturo Vidal', 'Chile', 'mediocampista'),
        ('Charles Aránguiz', 'Chile', 'mediocampista'),
        ('Erick Pulgar', 'Chile', 'mediocampista'),
        ('Marcelino Núñez', 'Chile', 'mediocampista'),
        ('Diego Valdés', 'Chile', 'mediocampista'),
        ('Darío Osorio', 'Chile', 'mediocampista'),
        ('Alexis Sánchez', 'Chile', 'delantero'),
        ('Eduardo Vargas', 'Chile', 'delantero'),
        ('Ben Brereton Díaz', 'Chile', 'delantero'),
        ('Víctor Dávila', 'Chile', 'delantero'),
        ('Carlos Palacios', 'Chile', 'delantero'),
        ('Alexander Aravena', 'Chile', 'delantero'),
        ('Rodrigo Echeverría', 'Chile', 'mediocampista')
    """)

    # Players - Paraguay
    op.execute("""
        INSERT INTO players (name, country, position) VALUES
        ('Antony Silva', 'Paraguay', 'arquero'),
        ('Alfaro Aguilar', 'Paraguay', 'arquero'),
        ('Roberto Fernández', 'Paraguay', 'arquero'),
        ('Gustavo Gómez', 'Paraguay', 'defensor'),
        ('Junior Alonso', 'Paraguay', 'defensor'),
        ('Omar Alderete', 'Paraguay', 'defensor'),
        ('Alberto Espínola', 'Paraguay', 'defensor'),
        ('Robert Rojas', 'Paraguay', 'defensor'),
        ('Fabián Balbuena', 'Paraguay', 'defensor'),
        ('Matías Espinoza', 'Paraguay', 'defensor'),
        ('Miguel Almirón', 'Paraguay', 'mediocampista'),
        ('Mathías Villasanti', 'Paraguay', 'mediocampista'),
        ('Andrés Cubas', 'Paraguay', 'mediocampista'),
        ('Óscar Romero', 'Paraguay', 'mediocampista'),
        ('Hernesto Caballero', 'Paraguay', 'mediocampista'),
        ('Julio Enciso', 'Paraguay', 'mediocampista'),
        ('Antonio Sanabria', 'Paraguay', 'delantero'),
        ('Ángel Romero', 'Paraguay', 'delantero'),
        ('Adam Bareiro', 'Paraguay', 'delantero'),
        ('Ramón Sosa', 'Paraguay', 'delantero'),
        ('Alex Arce', 'Paraguay', 'delantero'),
        ('Derlis González', 'Paraguay', 'delantero'),
        ('Diego Gómez', 'Paraguay', 'mediocampista')
    """)


def downgrade():
    op.execute("DELETE FROM players")
    op.execute("DELETE FROM match_days")
    op.execute("DELETE FROM users WHERE email = 'admin@grandt.com'")

#pragma warning( disable : 4996 ) 

 
#include <cstdlib>
#include <vector>
#include <iostream>
#include <string>
#include "G2D.h"
#include <algorithm>
 

// touche P   : mets en pause
// touche ESC : ferme la fenêtre et quitte le jeu


///////////////////////////////////////////////////////////////////////////////
//
//    Données du jeu - structure instanciée dans le main


struct Xenon
{
	V2 pos;
	V2 size;
	int IdSpriteNormal;
	int IdSpriteLeft;
	int IdSpriteRight;
	int IdBackground;
	int IdMechanttexture;
	int IdMissiletexture;

	Xenon()
	{
		pos = V2(300, 50);
		size = V2(32, 27);
	}

	void InitTextures()
	{
		IdSpriteNormal = G2D::ExtractTextureFromPNG("./xenon.png", Transparency::UpperLeft);
		IdSpriteLeft   = G2D::ExtractTextureFromPNG("./xenonLeft.png", Transparency::UpperRight);
		IdSpriteRight  = G2D::ExtractTextureFromPNG("./xenonRight.png", Transparency::UpperRight);
		int zoom = 3;
		size = size * zoom;
	}
};


struct GameData
{
	int     idFrame    = 0;
	int     HeightPix  = 800;          // hauteur de la fenêtre de jeu
	int     WidthPix   = 600;          // largeur de la fenêtre de jeu
	bool    isGameOver = false;
	bool    isGameStarted = false;

	vector<V2> Missiles;         // Liste des missiles
	vector<V2> Enemies;
	 
	vector<V2> PreviousPos;  // stocke les dernières positions de la boule
	vector<std::pair<V2, int>> Explosions; // Position + frames restantes
    int IdExplosionTexture;
	Xenon X;

	GameData()
	{
		PreviousPos.resize(50); // stocke les 50 dernières positions connues 
	}

};

// 0 pas d'intersection
// 1/2/3 intersection entre le segment AB et le cercle de rayon r
int CollisionSegCir(V2 A, V2 B, float r, V2 C)
{
	V2 AB = B - A;
	V2 T = AB;
	T.normalize();
	float d = prodScal(T, C - A);
	if (d > 0 && d < AB.norm())
	{
		V2 P = A + d * T; // proj de C sur [AB]
		V2 PC = C - P;
		if (PC.norm() < r) return 2;
		else               return 0;
	}
	if ((C - A).norm() < r) return 1;
	if ((C - B).norm() < r) return 3;
	return 0;
}


 


///////////////////////////////////////////////////////////////////////////////
//
// 
//     fonction de rendu - reçoit en paramètre les données du jeu par référence



void render(const GameData & G)
{

	G2D::clearScreen(Color::Black);
	G2D::drawRectWithTexture(G.X.IdBackground, V2(0, 0), V2(G.WidthPix, G.HeightPix));

	for (const auto& m : G.Missiles)
	G2D::drawRectWithTexture(G.X.IdMissiletexture, m - V2(7.5f, 15.0f), V2(15, 30)); // ajuste la taille à ton image
	
	if (!G.isGameStarted)
    {
        G2D::drawStringFontRoman(V2(120, 400), "Press D to start", 50.0f, 30.0f, Color::White);
    }

	if (G.isGameOver) {
		G2D::drawStringFontRoman(V2(200, 400), "Game Over", 50.0f, 30.0f, Color::White);
	}

	int idsprite = G.X.IdSpriteNormal;
	if (G2D::isKeyPressed(Key::LEFT))  idsprite = G.X.IdSpriteLeft;
	if (G2D::isKeyPressed(Key::RIGHT)) idsprite = G.X.IdSpriteRight;
	G2D::drawRectWithTexture(idsprite, G.X.pos, G.X.size);

	for (const auto& e : G.Enemies)
    G2D::drawRectWithTexture(G.X.IdMechanttexture, e - V2(27.5f, 22.5f), V2(55, 45));

	for (const auto& e : G.Explosions) {
		G2D::drawRectWithTexture(G.IdExplosionTexture, e.first - V2(32, 32), V2(64, 64));
	}

	G2D::Show();
}

	
///////////////////////////////////////////////////////////////////////////////
//
//
//      Gestion de la logique du jeu - reçoit en paramètre les données du jeu par référence



void Logic(GameData & G) // appelé 20 fois par seconde
{
	if (G.isGameOver) return;

	G.idFrame += 1;

// Déplacement joueur
if (G2D::isKeyPressed(Key::LEFT))  G.X.pos.x -= 5;
if (G2D::isKeyPressed(Key::RIGHT)) G.X.pos.x += 5;

if (!G.isGameStarted)
    {
        // Si la touche D est pressée, démarrer le jeu
        if (G2D::isKeyPressed(Key::D))
        {
            G.isGameStarted = true;
        }
        return;  // Ne pas exécuter la logique du jeu si le jeu n'est pas encore commencé
    }

// Tir missile (une seule fois par appui)
static bool lastS = false;
bool nowS = G2D::isKeyPressed(Key::S);

// Tir uniquement au moment où on presse la touche S
if (nowS && !lastS) {
    // On crée le missile à la position du joueur
	V2 missileStart = G.X.pos + V2(G.X.size.x / 2, G.X.size.y);
	G.Missiles.push_back(missileStart);
}
lastS = nowS;

// Mise à jour missiles
for (int i = 0; i < G.Missiles.size(); i++) {
    G.Missiles[i].y += 10;  // Décrémenter Y pour que les missiles descendent
}

// Supprimer missiles hors écran
G.Missiles.erase(remove_if(G.Missiles.begin(), G.Missiles.end(),
    [&](V2 m) { return m.y < 0; }), G.Missiles.end());

// Spawn ennemis
if (G.idFrame % 100 == 0) {
    G.Enemies.push_back(V2(rand() % G.WidthPix, 700));
}
// Mise à jour ennemis
for (int i = 0; i < G.Enemies.size(); i++) {
    G.Enemies[i].y -= 2;
}

// Collisions missile <-> ennemi
for (int i = 0; i < G.Missiles.size(); i++) {
    for (int j = 0; j < G.Enemies.size(); j++) {
        if ((G.Missiles[i] - G.Enemies[j]).norm() < 20) {
			V2 explosionPos = G.Enemies[j];
			G.Missiles.erase(G.Missiles.begin() + i);
			G.Enemies.erase(G.Enemies.begin() + j);
			G.Explosions.push_back(std::make_pair(explosionPos, 50));
			goto skipCollision; // éviter crash après erase
        }
    }
}

skipCollision:

for (const auto& e : G.Enemies) {
    // Calcul des centres des objets
    V2 vaisseauCentre = G.X.pos + V2(G.X.size.x / 2, G.X.size.y / 2);  // Centre du vaisseau
    V2 ennemiCentre = e;  // Centre de l'ennemi (l'ennemi est un point ici)

    // Distance entre les centres des deux objets
    float distance = (vaisseauCentre - ennemiCentre).norm();

    // Si la distance est inférieure à une valeur seuil, alors il y a collision
    float seuilCollision = 20;  // Seuil que tu peux ajuster pour la collision

    if (distance < seuilCollision) {
        std::cerr << "ERREUR : collision avec ennemi" << std::endl;
        G.isGameOver = true;
    }
}

for (int i = 0; i < G.Explosions.size(); ++i) {
	G.Explosions[i].second--;
}
G.Explosions.erase(remove_if(G.Explosions.begin(), G.Explosions.end(),
	[](const std::pair<V2, int>& e) { return e.second <= 0; }), G.Explosions.end());
}
 

///////////////////////////////////////////////////////////////////////////////
//
//
//        Démarrage de l'application



int main(int argc, char* argv[])
{
	GameData G;   // instanciation de l'unique objet GameData qui sera passé aux fonctions render et logic

	G2D::initWindow(V2(G.WidthPix, G.HeightPix), V2(200, 200), string("Shooter 600 !!"));


	int callToLogicPerSec = 50;  // si vous réduisez cette valeur => ralentit le jeu
	
	G.X.InitTextures();

	G.X.IdMissiletexture = G2D::ExtractTextureFromPNG("./missile00.png", Transparency::UpperLeft);


	G.X.IdMechanttexture = G2D::ExtractTextureFromPNG("./ship.png", Transparency::UpperLeft);

	G.X.IdBackground = G2D::ExtractTextureFromPNG("./fond.png", Transparency::None);

	G.IdExplosionTexture = G2D::ExtractTextureFromPNG("./explosion.png", Transparency::UpperLeft);


	G2D::Run(Logic, render, G, callToLogicPerSec,true);
}






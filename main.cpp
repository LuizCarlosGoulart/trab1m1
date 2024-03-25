#include <iostream>
#include <GL/freeglut.h>
#include <vector>
#include <cmath>

using vertice = std::tuple<double, double, double>;
using lista_vertices = std::vector<vertice>;
using aresta = std::pair<int, int>;
using lista_arestas = std::vector<aresta>;

// Estrutura do Cubo
struct Cubo {
    vertice posicao; // Centro do cubo
    vertice escala; // Escala em x, y, z
    double rotacao[3]; // Rotação em torno dos eixos x, y, z
    lista_vertices vertices;
    lista_arestas arestas;
};

Cubo criar_cubo(double posicao_x, double posicao_y, double posicao_z, double tamanho_aresta);
void desenhar(Cubo cubo);
void transladar(Cubo& cubo, double dx, double dy, double dz);
void escalar(Cubo& cubo, double escala_x, double escala_y, double escala_z);
void rotacionar(Cubo& cubo, double angulo_x, double angulo_y, double angulo_z);
void display();
void keyboard(unsigned char key, int x, int y);
void keyboard_special(int key, int x, int y);
void redraw(int value);

Cubo cubo;
int delay = 10;

int main(int argc, char** argv) {
    cubo = criar_cubo(0.0, 0.0, 0.0, 50.0);

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
    glutInitWindowSize(512, 512);
    glutCreateWindow("Cubo 3D");
    glEnable(GL_DEPTH_TEST);
    glClearColor(1.0, 1.0, 1.0, 1.0);

    // Definir a projeção perspectiva e a câmera
    glMatrixMode(GL_PROJECTION);
    gluPerspective(45.0, 1.0, 1.0, 400.0);
    glMatrixMode(GL_MODELVIEW);
    gluLookAt(200.0, 200.0, 200.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);

    glutDisplayFunc(display);
    glutKeyboardFunc(keyboard);
    glutSpecialFunc(keyboard_special);
    glutIdleFunc(display);

    glutMainLoop();

    return 0;
}

// Funções de criar cubo, desenhar, transladar, escalar, rotacionar, display, keyboard, keyboard_special, e redraw serão definidas aqui

Cubo criar_cubo(double posicao_x, double posicao_y, double posicao_z, double tamanho_aresta) {
    Cubo cubo;
    double meio = tamanho_aresta / 2.0;
    
    // Definindo vértices baseado no centro e tamanho de aresta
    cubo.vertices = {
        {posicao_x - meio, posicao_y - meio, posicao_z - meio},
        {posicao_x + meio, posicao_y - meio, posicao_z - meio},
        {posicao_x + meio, posicao_y + meio, posicao_z - meio},
        {posicao_x - meio, posicao_y + meio, posicao_z - meio},
        {posicao_x - meio, posicao_y - meio, posicao_z + meio},
        {posicao_x + meio, posicao_y - meio, posicao_z + meio},
        {posicao_x + meio, posicao_y + meio, posicao_z + meio},
        {posicao_x - meio, posicao_y + meio, posicao_z + meio}
    };

    // Definindo arestas que conectam os vértices
    cubo.arestas = {
        {0, 1}, {1, 2}, {2, 3}, {3, 0},
        {4, 5}, {5, 6}, {6, 7}, {7, 4},
        {0, 4}, {1, 5}, {2, 6}, {3, 7}
    };

    // Inicializando as propriedades de transformação
    cubo.posicao = {posicao_x, posicao_y, posicao_z};
    cubo.escala = {1.0, 1.0, 1.0};
    cubo.rotacao[0] = cubo.rotacao[1] = cubo.rotacao[2] = 0.0;

    return cubo;
}

void desenhar(Cubo cubo) {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glColor3f(0.0, 0.0, 0.0); // Cor preta para o wireframe
    glBegin(GL_LINES);
    for (const auto& aresta : cubo.arestas) {
        auto& v1 = cubo.vertices[aresta.first];
        auto& v2 = cubo.vertices[aresta.second];
        glVertex3d(std::get<0>(v1), std::get<1>(v1), std::get<2>(v1));
        glVertex3d(std::get<0>(v2), std::get<1>(v2), std::get<2>(v2));
    }
    glEnd();
    glutSwapBuffers();
}

void transladar(Cubo& cubo, double dx, double dy, double dz) {
    std::get<0>(cubo.posicao) += dx;
    std::get<1>(cubo.posicao) += dy;
    std::get<2>(cubo.posicao) += dz;
    for (auto& vertice : cubo.vertices) {
        std::get<0>(vertice) += dx;
        std::get<1>(vertice) += dy;
        std::get<2>(vertice) += dz;
    }
}

void escalar(Cubo& cubo, double escala_x, double escala_y, double escala_z) {
    cubo.escala = {escala_x, escala_y, escala_z};
    for (auto& vertice : cubo.vertices) {
        std::get<0>(vertice) = std::get<0>(cubo.posicao) + (std::get<0>(vertice) - std::get<0>(cubo.posicao)) * escala_x;
        std::get<1>(vertice) = std::get<1>(cubo.posicao) + (std::get<1>(vertice) - std::get<1>(

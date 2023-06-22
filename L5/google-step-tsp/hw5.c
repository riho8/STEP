#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

typedef struct {
    double x;
    double y;
} City;

void print_tour(int* tour, int N) {
    for (int i = 0; i < N; i++) {
        printf("%d ", tour[i]);
    }
    printf("\n");
}
double distance(City a, City b) {
    return hypot(a.x - b.x, a.y - b.y);
}

double total_distance(int* tour, double** dist, int N) {
    double distance = 0.0;
    for (int i = 0; i < N - 1; i++) {
        distance += dist[tour[i]][tour[i + 1]];
    }
    distance += dist[tour[N - 1]][tour[0]];
    return distance;
}

int* greedy(double** dist, int start, int N) {
    int* tour = (int*)malloc(N * sizeof(int));
    int* unvisited = (int*)malloc(N * sizeof(int));
    int tourIndex = 0;
    for (int i = 0; i < N; i++) {
        unvisited[i] = 1;
    }
    unvisited[start] = 0;
    tour[tourIndex++] = start;
    while (1) {
        int current = tour[tourIndex - 1];
        int next_city = -1;
        double min_dist = -1.0;
        for (int i = 0; i < N; i++) {
            if (unvisited[i] == 1 && (next_city == -1 || dist[current][i] < min_dist)) {
                next_city = i;
                min_dist = dist[current][i];
            }
        }
        if (next_city == -1) {
            break;
        }
        tour[tourIndex++] = next_city;
        unvisited[next_city] = 0;
    }
    free(unvisited);
    return tour;
}

int* swap_for_two_opt(int* tour, int city1, int city2,int N) {
    int* new_tour = (int*)malloc(N * sizeof(int));
    if (!new_tour) return NULL;
    int i;
    // Copy elements before city1
    for (i = 0; i < city1; i++) {
        new_tour[i] = tour[i];
    }

    // Reverse elements between city1 and city2
    int k = 0;
    for (i = city1; i < city2; i++) {
        new_tour[i] = tour[city2 - k - 1];
        k++;
    }

    // Copy elements after city2
    for (i = city2; i < N; i++) {
        new_tour[i] = tour[i];
    }

    return new_tour;
}

int* two_opt(double** dist, int* tour, int N) {
    int improvementNeeded = 1;
    while (improvementNeeded) {
        improvementNeeded = 0;
        for (int city1 = 0; city1 < N - 1; city1++) {
            for (int city2 = city1 + 1; city2 < N; city2++) {
                int* new_tour = swap_for_two_opt(tour, city1, city2,N);
                double new_distance = total_distance(new_tour, dist, N);
                if (new_distance < total_distance(tour, dist, N)) {
                    free(tour);
                    tour = new_tour;
                    improvementNeeded = 1;
                    break;
                }
                free(new_tour);
            }
            if (improvementNeeded) {
                break;
            }
        }
    }
    return tour;
}

void shuffle(int array[], unsigned int size) {
    unsigned int i, j;
    int tmp;

    /* シャッフル範囲の末尾を設定 */
    i = size - 1;

    while (i > 0) {
        /* シャッフル範囲（0〜i）からランダムに１つデータを選択 */
        j = rand() % (i + 1);

        /* ランダムに決めたデータとシャッフル範囲の末尾のデータを交換 */
        tmp = array[j];
        array[j] = array[i];
        array[i] = tmp;

        /* シャッフル範囲を狭める */
        i--;
    } 
}

int* solve(City* cities, int N) {
    double min_dist = INFINITY;

    double** dist = (double**)malloc((N) * sizeof(double*));
    if(!dist) return NULL;
    for (int i = 0; i < N; i++) {
        dist[i] = (double*)malloc((N) * sizeof(double));
        if(!dist[i]) return NULL;
        for (int j = 0; j < N; j++) {
            double ans =  distance(cities[i], cities[j]);
            dist[i][j] = ans;
        }
    }
    int topLeft =0;
    int topRight =0;
    int bottomLeft =0;
    int bottomRight =0;

    for (int i = 1; i < N; i++) {
        if (cities[i].x < cities[topLeft].x)
            topLeft = i;
        if (cities[i].x > cities[topRight].x)
            topRight = i;
        if (cities[i].y < cities[bottomLeft].y)
            bottomLeft = i;
        if (cities[i].y > cities[bottomRight].y)
            bottomRight = i;
    }
    int corners[4] = {topLeft, topRight, bottomLeft, bottomRight};
    int* best_tour = (int*)malloc(N * sizeof(int));
    for (int i = 0; i < 4; i++) {
        int start = corners[i];
        printf("start: %d\n", start);
        int* tour = greedy(dist, start, N);
        tour = two_opt(dist, tour, N);
        double current_dist = total_distance(tour, dist, N);
        if (current_dist < min_dist) {
            min_dist = current_dist;
            for (int i = 0; i < N; i++) {
                best_tour[i] = tour[i];
            }
        }
        free(tour);
    }
    printf("Minimum distance: %lf\n", min_dist);
    for (int i = 0; i < N; i++) {
        free(dist[i]);
    }
    free(dist);

    return best_tour;
}

int my_strcmp(const char* str1, const char* str2) {
    int i = 0;
    while (str1[i] != '\0' && str2[i] != '\0') {
        if (str1[i] !=str2[i])
            return str1[i] - str2[i];
        i++;
    }
    if (str1[i] == '\0' && str2[i] == '\0')
        return 0;
    else
        return -1;
}

int main(int argc, char** argv) {
    if (argc <= 1) {
        printf("No input file provided.\n");
        return 1;
    }
    FILE* file = fopen(argv[1], "r");
    if (file == NULL) {
        printf("Failed to open input file.\n");
        return 1;
    }
    int N;

    int strcmp_rtn = my_strcmp(argv[1],"input_0.csv");

    if (strcmp_rtn == 0)
        N = 5;
    else if (strcmp_rtn == 1)
        N = 8;
    else if (strcmp_rtn == 2)
        N = 16;
    else if (strcmp_rtn == 3)
        N = 64;
    else if (strcmp_rtn == 4)
        N = 128;
    else if (strcmp_rtn == 5)
        N = 512;
    else if (strcmp_rtn == 6)
        N = 2048;
    else if (strcmp_rtn == 7)
        N = 4096;
    
    City* cities = (City*)malloc(N * sizeof(City));

    
    char str[100];
    fgets(str, N, file);
    for (int i = 0; i < N ; i++) {
        fscanf(file, "%lf,%lf\n", &cities[i].x, &cities[i].y);
    }
    fclose(file);
    int* tour = solve(cities, N);
    printf("index\n");
    for (int i = 0; i < N; i++) {
        printf("%d\n", tour[i]);
    }

    free(cities);
    free(tour);

    return 0;
}

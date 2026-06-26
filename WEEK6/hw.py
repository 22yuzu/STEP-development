#!/usr/bin/env python3
import math
import sys
from common import print_tour, read_input


# 2つの都市のユークリッド距離を計算する。
# 時間計算量: O(1)
def distance(city1, city2):
    return math.hypot(city1[0] - city2[0], city1[1] - city2[1])


# すべての都市ペアの距離を先に計算して、表として保存しておく。
# これにより、2-opt や Or-opt の中で距離を毎回計算せずに、
# dist[i][j] のように O(1) で距離を取得できる。
#
# n = 都市数 とすると、
# 時間計算量: O(n^2)
# 空間計算量: O(n^2)
def build_distance_table(cities):
    n = len(cities)
    dist = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            d = distance(cities[i], cities[j])
            dist[i][j] = d
            dist[j][i] = d

    return dist


# tour 全体の距離を計算する。
# TSP では最後の都市から最初の都市に戻るので、
# tour[-1] から tour[0] への距離も足している。
#
# 時間計算量: O(n)
def tour_length(tour, dist):
    n = len(tour)
    total = 0.0

    for i in range(n):
        total += dist[tour[i]][tour[(i + 1) % n]]

    return total


# nearest neighbor 法で初期ルートを作る。
# start_city から始めて、毎回「現在地から一番近い未訪問都市」を選ぶ。
#
# 時間計算量: O(n^2)
# 空間計算量: O(n)
def nearest_neighbor(cities, dist, start_city):
    n = len(cities)

    visited = [False] * n
    tour = [start_city]
    visited[start_city] = True

    current_city = start_city

    for _ in range(n - 1):
        nearest_city = None
        nearest_distance = float("inf")

        for city in range(n):
            if not visited[city] and dist[current_city][city] < nearest_distance:
                nearest_distance = dist[current_city][city]
                nearest_city = city

        tour.append(nearest_city)
        visited[nearest_city] = True
        current_city = nearest_city

    return tour


# 複数の始点から nearest neighbor を実行し、
# その中で一番距離が短い tour を選ぶ。
#
# nearest neighbor は始点によって結果が大きく変わることがあるため、
# 複数の始点を試すことで、より良い初期解を得やすくしている。
def multi_start_nearest_neighbor(cities, dist):
    n = len(cities)

    if n == 0:
        return []

    # すべての都市を始点にすると、大きい入力では重くなりすぎる。
    # そのため、都市数に応じて試す始点の数を調整する。
    if n <= 50:
        start_count = n
    elif n <= 300:
        start_count = 12
    elif n <= 1000:
        start_count = 6
    else:
        start_count = 3

    starts = []
    for i in range(start_count):
        starts.append((i * n) // start_count)

    # 念のため、重複した始点を取り除く。
    starts = sorted(set(starts))

    best_tour = None
    best_length = float("inf")

    for start in starts:
        tour = nearest_neighbor(cities, dist, start)
        length = tour_length(tour, dist)

        if length < best_length:
            best_length = length
            best_tour = tour

    return best_tour


# 2-opt によって tour を改善する。
#
# 2-opt では、2本の辺を選ぶ。
#   a -> b
#   c -> d
#
# そして、それを以下のようにつなぎ替える。
#   a -> c
#   b -> d
#
# 新しいつなぎ方の方が短ければ、
# b から c までの区間を反転して tour を更新する。
#
# 2-opt は、交差している辺や非効率なつなぎ方を改善するのに有効。
#
# 実用上の時間計算量:
#   O(k n^2)
#   k は改善のために繰り返した回数。
def two_opt(tour, dist):
    n = len(tour)

    if n < 4:
        return tour

    improved = True

    while improved:
        improved = False

        for i in range(n - 1):
            a = tour[i]
            b = tour[(i + 1) % n]

            for j in range(i + 2, n):
                # 最初の辺と最後の辺を同時に選ぶと、
                # cycle 上で隣り合う辺を選んでいることになるためスキップする。
                if i == 0 and j == n - 1:
                    continue

                c = tour[j]
                d = tour[(j + 1) % n]

                current_distance = dist[a][b] + dist[c][d]
                new_distance = dist[a][c] + dist[b][d]

                if new_distance < current_distance:
                    # b から c までの区間を反転する。
                    tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                    improved = True
                    break

            # tour を変更したら、いったん探索を最初からやり直す。
            # これにより実装をシンプルに保てる。
            if improved:
                break

    return tour


# Or-opt のうち、1都市を移動するバージョンで tour を改善する。
#
# Or-opt は、ある都市を現在の位置から取り除き、
# 別の位置に挿入することで tour が短くなるなら更新する方法。
#
# 例:
#   変更前: ... a -> b -> c ... x -> y ...
#   変更後: ... a -> c ... x -> b -> y ...
#
# この例では、都市 b を a と c の間から取り除き、
# x と y の間に挿入している。
#
# 2-opt では直しにくい「都市の位置そのものが微妙」なケースを改善できる。
#
# 実用上の時間計算量:
#   O(k n^2)
#   k は改善のために繰り返した回数。
def or_opt_one_city(tour, dist):
    n = len(tour)

    if n < 4:
        return tour

    improved = True

    while improved:
        improved = False

        for i in range(n):
            a = tour[i - 1]
            b = tour[i]
            c = tour[(i + 1) % n]

            # b を a と c の間から取り除いたときの距離の変化量。
            # 新しく a -> c をつなぎ、
            # 元々あった a -> b と b -> c を消す。
            remove_delta = dist[a][c] - dist[a][b] - dist[b][c]

            for j in range(n):
                # b の直後に b を入れることはできないのでスキップする。
                if j == i:
                    continue

                # b を元々の直前の都市の後ろに戻すだけだと、
                # tour が変わらないのでスキップする。
                if j == (i - 1) % n:
                    continue

                x = tour[j]
                y = tour[(j + 1) % n]

                # b を x と y の間に挿入したときの距離の変化量。
                # 元々あった x -> y を消し、
                # 新しく x -> b と b -> y を追加する。
                insert_delta = dist[x][b] + dist[b][y] - dist[x][y]

                total_delta = remove_delta + insert_delta

                if total_delta < 0:
                    moved_city = tour.pop(i)

                    # i < j の場合、pop によって j の位置が1つ左にずれる。
                    # そのため、insert する位置を調整する。
                    if i < j:
                        tour.insert(j, moved_city)
                    else:
                        tour.insert(j + 1, moved_city)

                    improved = True
                    break

            # tour を変更したら、いったん探索を最初からやり直す。
            if improved:
                break

    return tour


# メインの解法関数。
#
# 方針:
#   1. multi-start nearest neighbor で良さそうな初期解を作る。
#   2. 2-opt で tour を改善する。
#   3. Or-opt で都市の位置を動かしてさらに改善する。
#   4. 最後にもう一度 2-opt を行い、Or-opt 後に残った無駄を取り除く。
def solve(cities):
    n = len(cities)

    # エッジケースへの対応。
    if n == 0:
        return []
    if n == 1:
        return [0]

    dist = build_distance_table(cities)

    tour = multi_start_nearest_neighbor(cities, dist)
    tour = two_opt(tour, dist)
    tour = or_opt_one_city(tour, dist)
    tour = two_opt(tour, dist)

    return tour


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 solver.py input_file")
        sys.exit(1)

    cities = read_input(sys.argv[1])
    tour = solve(cities)
    print_tour(tour)

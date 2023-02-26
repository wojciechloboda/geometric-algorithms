import csv

import matplotlib.pyplot as plt


def main():
    names = [
        "normal_dist.csv",
        "circle.csv",
        "cross.csv",
        "grid.csv",
        "on_rectangle.csv",
        "outliers.csv",
    ]
    for filename in names:
        sizes = []
        kd_build = []
        quad_build = []
        kd_search = []
        quad_search = []
        with open(filename) as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
                sizes.append(float(row[0]))
                kd_build.append(float(row[1]))
                quad_build.append(float(row[2]))
                kd_search.append(float(row[3]))
                quad_search.append(float(row[4]))
            plt.plot(sizes, kd_build, label="KD-Tree")
            plt.scatter(sizes, kd_build)
            plt.plot(sizes, quad_build, label="QuadTree")
            plt.scatter(sizes, quad_build)
            plt.legend()
            plt.xlabel("Rozmiar danych")
            plt.ylabel("Czas w sekundach")
            plt.savefig("build_time/"+filename.split(".")[0] + "_build")
            plt.clf()

            plt.plot(sizes, kd_search, label="KD-Tree")
            plt.scatter(sizes, kd_search)
            plt.plot(sizes, quad_search, label="QuadTree")
            plt.scatter(sizes, quad_search)
            plt.legend()
            plt.xlabel("Rozmiar danych")
            plt.ylabel("Czas w sekundach")
            plt.savefig("search_time/"+filename.split(".")[0] + "_search")
            plt.clf()


if __name__ == "__main__":
    main()

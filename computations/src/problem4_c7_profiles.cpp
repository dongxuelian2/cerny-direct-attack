// Complete eight-state action domain for the uniform C7 reduction.
// Default: enumerate cycle kernel partitions and injective output assignments.
// --literal: independently enumerate all 8^8 maps and filter their kernels.
#include <algorithm>
#include <array>
#include <iostream>
#include <numeric>
#include <set>
#include <string>
#include <vector>
using Row = std::array<int, 15>; // eight transition values, then seven images

int main(int argc, char **argv) {
  const bool literal = argc == 2 && std::string(argv[1]) == "--literal";
  if (argc > 2 || (argc == 2 && !literal))
    return 2;
  std::vector<int> family;
  for (int mask = 0; mask < 128; ++mask) {
    int weight = 0;
    bool independent = true;
    for (int i = 0; i < 7; ++i) {
      weight += (mask >> i) & 1;
      if ((mask >> i & 1) && (mask >> ((i + 1) % 7) & 1))
        independent = false;
    }
    if (weight == 3 && independent)
      family.push_back(mask | 128);
  }
  if (family.size() != 7)
    return 3;
  std::set<Row> accepted;
  long long examined = 0, domain = 0;
  auto record = [&](const std::array<int, 8> &f) {
    ++domain;
    Row row{};
    std::copy(f.begin(), f.end(), row.begin());
    int safe = 0;
    for (int i = 0; i < 7; ++i) {
      int image = 0;
      for (int v = 0; v < 8; ++v)
        if (family[i] >> v & 1)
          image |= 1 << f[v];
      auto it = std::find(family.begin(), family.end(), image);
      row[8 + i] = it == family.end() ? 7 : int(it - family.begin());
      safe += row[8 + i] != 7;
    }
    if (safe >= 5)
      accepted.insert(row);
  };
  if (literal) {
    for (int code = 0; code < (1 << 24); ++code) {
      ++examined;
      int x = code, outputs = 0;
      std::array<int, 8> f{};
      for (int &value : f) {
        value = x % 8;
        x /= 8;
        outputs |= 1 << value;
      }
      int rank = 0;
      for (int i = 0; i < 8; ++i)
        rank += outputs >> i & 1;
      if (rank < 6)
        continue;
      bool good = true;
      for (int u = 0; u < 8 && good; ++u)
        for (int v = u + 1; v < 8; ++v)
          if (f[u] == f[v] && !(v < 7 && (v == u + 1 || (u == 0 && v == 6)))) {
            good = false;
            break;
          }
      if (good)
        record(f);
    }
  } else {
    for (int mask = 0; mask < 128; ++mask) {
      int used = 0, count = 0;
      bool matching = true;
      std::array<int, 8> block{};
      std::iota(block.begin(), block.end(), 0);
      for (int i = 0; i < 7; ++i)
        if (mask >> i & 1) {
          ++count;
          int j = (i + 1) % 7;
          if ((used >> i & 1) || (used >> j & 1))
            matching = false;
          used |= (1 << i) | (1 << j);
          block[j] = i;
        }
      if (!matching || count > 2)
        continue;
      std::vector<int> blocks(block.begin(), block.end());
      std::sort(blocks.begin(), blocks.end());
      blocks.erase(std::unique(blocks.begin(), blocks.end()), blocks.end());
      std::array<int, 8> output{};
      std::iota(output.begin(), output.end(), 0);
      do {
        ++examined;
        std::array<int, 8> f{};
        for (int i = 0; i < 8; ++i)
          f[i] = output[std::find(blocks.begin(), blocks.end(), block[i]) -
                        blocks.begin()];
        record(f);
        // Each injection appears once, irrespective of unused output order.
        std::reverse(output.begin() + blocks.size(), output.end());
      } while (std::next_permutation(output.begin(), output.end()));
    }
  }
  std::cerr << "examined=" << examined << " domain=" << domain
            << " accepted=" << accepted.size() << '\n';
  if (domain != 604800 || accepted.size() != 1484)
    return 4;
  for (const auto &row : accepted) {
    for (int i = 0; i < 15; ++i)
      std::cout << (i ? " " : "") << row[i];
    std::cout << '\n';
  }
}

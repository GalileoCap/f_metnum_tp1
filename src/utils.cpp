#include "utils.h"
#include <chrono>
#include <iomanip>

long get_time() { //U: Returns the current time in milliseconds
  auto start = std::chrono::system_clock::now();
  return std::chrono::duration_cast<std::chrono::nanoseconds>(start.time_since_epoch()).count();
}

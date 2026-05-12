# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

import cython
from libc.stdlib cimport malloc, free

cdef struct OrderC:
    double price
    double qty
    int is_buy

cdef class FastMatchingEngine:
    """
    A highly optimized Cython matching engine for nanosecond-level latency.
    Bypasses the Python GIL for core matching logic.
    """
    cdef OrderC* buy_orders
    cdef OrderC* sell_orders
    cdef int buy_count
    cdef int sell_count
    cdef int capacity

    def __cinit__(self, int capacity=100000):
        self.capacity = capacity
        self.buy_orders = <OrderC*> malloc(sizeof(OrderC) * capacity)
        self.sell_orders = <OrderC*> malloc(sizeof(OrderC) * capacity)
        self.buy_count = 0
        self.sell_count = 0

    def __dealloc__(self):
        free(self.buy_orders)
        free(self.sell_orders)

    @cython.cdivision(True)
    cpdef void insert_order(self, double price, double qty, bint is_buy):
        if is_buy:
            if self.buy_count < self.capacity:
                self.buy_orders[self.buy_count].price = price
                self.buy_orders[self.buy_count].qty = qty
                self.buy_orders[self.buy_count].is_buy = 1
                self.buy_count += 1
        else:
            if self.sell_count < self.capacity:
                self.sell_orders[self.sell_count].price = price
                self.sell_orders[self.sell_count].qty = qty
                self.sell_orders[self.sell_count].is_buy = 0
                self.sell_count += 1

    cpdef int match_orders(self):
        """
        Ultra-fast C-level matching loop.
        Returns the number of trades executed.
        """
        cdef int trades = 0
        cdef int i = 0
        cdef int j = 0
        
        while i < self.buy_count and j < self.sell_count:
            if self.buy_orders[i].price >= self.sell_orders[j].price:
                # Match found
                if self.buy_orders[i].qty <= self.sell_orders[j].qty:
                    self.sell_orders[j].qty -= self.buy_orders[i].qty
                    self.buy_orders[i].qty = 0
                    i += 1
                else:
                    self.buy_orders[i].qty -= self.sell_orders[j].qty
                    self.sell_orders[j].qty = 0
                    j += 1
                trades += 1
            else:
                break
        return trades

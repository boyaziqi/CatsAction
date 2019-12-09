package main

import "fmt"

func main() {
    var a []int = []int{6, 8, 2, 1, 4, 3, 5, 2, 10, 9, 7}
    QuitSort(a)
    fmt.Println(a)
}

func QuitSort(source []int) {
    sort(source, 0, len(source) - 1)
}

func sort(source []int, lo, hi int) {
    if hi<= lo {
        return
    }
    j := partition(source, lo, hi)
    fmt.Printf("kk=%d\n", j)
    sort(source, lo, j-1)
    sort(source, j+1, hi)
}

func partition(source []int, lo, hi int) int {
    var i, j int = lo, hi + 1
    var v int = source[lo]
    for {
        i += 1
        j -= 1
        fmt.Printf("i=%d,j=%d\n", i, j)
        for ; source[i] < v; i++{
            fmt.Printf("i=%d,soure=%d\n", i, source[i])
            if i == hi {
                break
            } 
        }
        for ; source[j] > v; j-- {
            fmt.Printf("j=%d,soure=%d\n", j, source[j])
            if j == lo {
                break
            }
        }
        if i >= j {
            break
        }
        source[i], source[j] = source[j], source[i]
    }
    source[lo], source[j] = source[j], source[lo]
    return j
}

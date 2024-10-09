#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <NIDAQmx.h>

// 入力を保持する構造体
typedef struct {
    int input_id;
    double input_value;
} Input;

// 関数プロトタイプ宣言
void* read_input(void* arg);
double process_inputs(Input inputs[], int num_inputs);

// スレッドごとに読み込む入力データの最大数
#define MAX_INPUTS 15

int main() {
    // 最大15個の入力を保持する配列
    Input inputs[MAX_INPUTS];
    
    pthread_t threads[MAX_INPUTS]; // スレッドIDを保持する配列
    int num_inputs = 10; // 入力の数 (可変に変更可能)
    
    // スレッドを生成し、入力を非同期に読み取る
    for (int i = 0; i < num_inputs; i++) {
        inputs[i].input_id = i; // 各入力のIDを設定
        if (pthread_create(&threads[i], NULL, read_input, (void*)&inputs[i])) {
            fprintf(stderr, "スレッド作成に失敗しました\n");
            return 1;
        }
    }
    
    // すべてのスレッドが終了するまで待つ
    for (int i = 0; i < num_inputs; i++) {
        pthread_join(threads[i], NULL);
    }
    
    // 取得した入力データを処理し、結果を返す
    double result = process_inputs(inputs, num_inputs);
    printf("最終的な処理結果: %f\n", result);
    
    return 0;
}

// 各入力を非同期に取得する関数
void* read_input(void* arg) {
    Input* input = (Input*)arg;
    
    // NIDAQmxを使って入力を取得 (ここではダミーでランダム値を設定)
    input->input_value = (double)(rand() % 100) / 10.0;
    printf("入力 %d の値: %f\n", input->input_id, input->input_value);
    
    return NULL;
}

// 入力データを処理して最終結果を返す関数
double process_inputs(Input inputs[], int num_inputs) {
    double sum = 0.0;
    for (int i = 0; i < num_inputs; i++) {
        sum += inputs[i].input_value;
    }
    
    // 平均を返す (処理内容は任意で変更可能)
    return sum / num_inputs;
}

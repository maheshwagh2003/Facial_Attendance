#include <iostream>

struct Node {
    int data;
    Node* left;
    Node* right;

    Node(int data) {
        this->data = data;
        this->left = nullptr;
        this->right = nullptr;
    }
};

class BinarySearchTree {
private:
    Node* root;

    Node* insert(Node* node, int data) {
        if (node == nullptr) {
            return new Node(data);
        }
        if (data < node->data) {
            node->left = insert(node->left, data);
        } else if (data > node->data) {
            node->right = insert(node->right, data);
        }
        return node;
    }

    void inorder(Node* node) {
        if (node == nullptr) {
            return;
        }
        inorder(node->left);
        std::cout << node->data << " ";
        inorder(node->right);
    }

public:
    BinarySearchTree() {
        this->root = nullptr;
    }

    void insert(int data) {
        root = insert(root, data);
    }

    void inorder() {
        inorder(root);
    }
};

int main() {
    BinarySearchTree bst;

    bst.insert(50);
    bst.insert(30);
    bst.insert(20);
    bst.insert(40);
    bst.insert(70);
    bst.insert(60);
    bst
}
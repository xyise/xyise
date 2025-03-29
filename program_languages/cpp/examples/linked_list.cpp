#include <iostream>

// Define the RateLink structure
struct RateLink {
    int value;
    RateLink* next;
};

// Function prototype for work_on
void work_on(const RateLink* X);

// Function to do something with the RateLink list
int do_somthing(const RateLink* X) {
    // Create a new RateLink object
    RateLink* newLink = new RateLink;
    newLink->value = 0; // Set the value of the new link (you can set it to any value you want)
    newLink->next = const_cast<RateLink*>(X); // Attach the new link to the beginning of the list
    // Pass the updated list to work_on
    work_on(newLink);

    RateLink newLink2{0, const_cast<RateLink*>(X)};
    work_on(&newLink2);

    // Clean up the new link if necessary (depends on the ownership and lifecycle of the list)
    // If work_on does not take ownership of the list, you may need to delete the newLink here
    // delete newLink;

    return 0;
}

// Example implementation of work_on function
void work_on(const RateLink* X) {
    // Print the linked list values
    const RateLink* current = X;
    while (current != nullptr) {
        std::cout << current->value << " ";
        current = current->next;
    }
    std::cout << std::endl;
}

// Example usage
int main() {
    // Create a simple linked list
    RateLink* link1 = new RateLink{1, nullptr};
    RateLink* link2 = new RateLink{2, link1};
    RateLink* link3 = new RateLink{3, link2};

    // Call do_somthing with the linked list
    do_somthing(link3);

    // Clean up the original linked list
    delete link1;
    delete link2;
    delete link3;

    return 0;
}
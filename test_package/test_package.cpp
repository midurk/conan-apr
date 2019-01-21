#include <cstdlib>
#include <iostream>

#include <apr_general.h>

int main()
{
    apr_status_t ret = apr_initialize();
    if (APR_SUCCESS != ret) {
        char reason[1024];
        apr_strerror(ret, reason, 1024);
        std::cerr << "Failed to initialize APR: " << reason;
        exit(ret);
    }
    
    std::cout << "Bincrafters\n";

    apr_terminate();
    
    return EXIT_SUCCESS;
}

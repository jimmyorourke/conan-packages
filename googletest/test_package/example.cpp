#include <string>

class Concrete
{
public:
    static std::string concat(const std::string& str1, const std::string& str2) {
        return str1 + str2;
    }
};

class IExample
{
public:
    virtual void func() = 0;
};

// Test

#include <gtest/gtest.h>
#include <gmock/gmock.h>

class MockExample : public IExample
{
public:
    MOCK_METHOD0(func, void());
};

TEST(FooTest, Static) {
    MockExample m;
    EXPECT_EQ(Concrete::concat("hello", "world"), "helloworld");
}

// No main - link with gmock_main instead

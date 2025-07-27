// talking with game dev friend who works in C++ about Enzo

int[] a;

TArray<int> users;

TArray<int> filter-active(const TArray<int>& list)
{
    // definition
    static const FName "Active";
}

TArray<int> sort-by(const TArray<int>& list, FName Sort)
{
    // definition
}

UObject, AActor, FStruct

const $age, $limbs, $height =

const UMyObject* MyOtherObjectInstance;

UMyObject const * const MyObjectInstance;

MyObjectInstance->age = 25;

MyObjectInstance = MyOtherInstance


TArray<int> Results = filter-active(users);
Results = SortBy(Results, "last")

int[] filter-active(int[]& chad, char[])

$emails-final: toUpper(
    join(
        filter(
            unique(
                map(
                    sort-by(
                        filter-active($users),
                        "last-name"
                    ),
                    get-email
                )
            ),
            is-work-email
        ),
        "; "
    )
);

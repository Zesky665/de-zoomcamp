## Week 2: Orchestration

#### Prerequisites

Make sure you have docker installed on your machine.

You can download it [here](https://www.docker.com/products/docker-desktop/).

### How to run the example

1. Navigate to the Week_1 directory.
```
cd Week_2
```

2. Build the docker images using docker-compose
```
docker-compose build
```

3. Run docker-compose:
```
docker-compose up
```

4. Once the Mage instance is running, use the script to run the pipeline.

```
python3 ingenst_quarter.py <year> <month>
```


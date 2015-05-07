## Image Servers setup instructions


Create a droplet. In the Applications section select "Docker". 
If you are using another cloud just create an instance and install "Docker"

Access the instance and create this folder if it doesn't exist

```
$ mkdir /var/www
```

Create a file called `Dockerfile` in that folder. Put the following contents in the file

```
FROM cydev/go
RUN go get github.com/chrislusf/seaweedfs/go/weed
EXPOSE 8080
EXPOSE 9333
VOLUME /data
ENTRYPOINT ["weed"]
```

Now run 
```
$ docker build .
```

If you run `$ docker images` you'll see the new docker image in the list:

```
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
<none>              <none>              <weed-image-id>        42 hours ago        783.5 MB
cydev/go            latest              9c6c2185c7c7        9 months ago        664.8 MB
```

Notice that there are two images.  cydev/go was the first step to get to the second one. Copy the IMAGE ID of the image on the top

Now you are ready to start the SeaweedFS MASTER and VOLUME instances

First start the MASTER
```
docker run -d -p <this-instance-ip-address>:9333:9333  -v /www/master <weed-image-id>  master -mdir="/www/master" -ip <this-instance-ip-address>
```

Check that it is running : `$ docker ps` . You should see something like this:
```
CONTAINER ID        IMAGE                 COMMAND             CREATED             STATUS              PORTS                                   NAMES
<this-container-id>        <this-image-id>:latest   "weed master"       5 seconds ago       Up 5 seconds        8080/tcp, <this-instance-ip-address>:9333->9333/tcp   stupefied_mcclintock
```

Then in your browser go to: `http://<master-instance-ip-address>:9333` . You should see SeaweedFS Master status page.

Start the SeaweedFS Volume server

```
docker run -d -p <this-instance-ip-address>:8080:8080 -v /www/images <weed-image-id> volume -dir="/www/images" -max=5  -mserver="<master-instance-ip-address>:9333" -ip <volume-instance-ip-address> -port=8080 &
```

In your browser go to : `http://<volume-instance-ip-address>:80`  . You'll see the SeaweedFS Volume status page. Also you should see the new rom in the "Topology" list in the Master status page

Note this: It is possible to run both the Master and the Volume server in the same instance but this defeats the whole idea of scalability. In production there should be one instance dedicated to the Master and N Volume instances.

#### Backup

SeaweedFS stores the images in volumes. It is possible to see the volume but it is not possible to see individual images. This is completely normal the same way you don't go to the *myd MySQL files trying to subtract some data directly. 

The backup script needs to go where the Docker Volumes (not the same as SeaweedFS volumes) is and back up the whole Folder that contains the volumes. 


#### Testing

Request an id to write a file
```
$ curl -X POST http://<master-instance-ip-address>:9333/dir/assign
{"count":1,"fid":"3,01637037d6","url":"<volume-instance-ip>:8080","publicUrl":"<volume-instance-ip>:8080"}
```

Send the file
```
$ curl -X PUT -F file=@/path/to/photo/myphoto.jpg http://<volume-instance-ip>/3,01637037d6
{"size": 43234}
```

Now try to reach the file using your browser
```
http://<volume-instance-ip>/3,01637037d6
```

If the image is there you are ready!




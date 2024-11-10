
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <inttypes.h>
#include <signal.h>

#define PORTS "55555"

int sock_fd, srvc_fd, fdmax=0;
fd_set master, read_fds;

void fonction_handler(void)
{
    int i;
    
    printf("Terminaison processus serveur\n");
    close(sock_fd);
    
    for(i=0; i<=fdmax; i++)
    {
        if(FD_ISSET(i, &read_fds)) {
            close(i);
        }
    }
    
    exit(0);
}

int main(int argc, char **argv)
{
  int num_cli=0;
  struct addrinfo s_init, *servinfo, *p;
  struct sockaddr client_addr;
  socklen_t s_taille;
  char msg[50];
  
  uint16_t taille_msg;
  char head[2];
  
  int i;

  
  // Association fonction de traitement au signal SIGINT
  signal(SIGINT, (__sighandler_t) fonction_handler);
  
  memset(&s_init, 0, sizeof(s_init));
  s_init.ai_family = AF_INET;
  s_init.ai_socktype = SOCK_STREAM;
  s_init.ai_flags = AI_PASSIVE;

  if (getaddrinfo(NULL, PORTS, &s_init, &servinfo) != 0) {
    fprintf(stderr, "Erreur getaddrinfo\n");
    exit(1);
  }
	  
  for(p = servinfo; p != NULL; p = p->ai_next) {
    if ((sock_fd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
      perror("Serveur: socket");
      continue;
    }

    if (bind(sock_fd, p->ai_addr, p->ai_addrlen) == -1) {
      close(sock_fd);
      perror("Serveur: erreur bind");
      continue;
    }
    break;
  }

  if (p == NULL) {
    fprintf(stderr, "Serveur: echec bind\n");
    exit(2);
  }
	  
  freeaddrinfo(servinfo);

  if (listen(sock_fd, 5) == -1) {
    perror("listen");
    exit(1);
  }

  FD_ZERO(&master);
  FD_ZERO(&read_fds);
  
  FD_SET(sock_fd, &master);
  fdmax=sock_fd;

  printf("Attente connexion client\n");
  
  while(1) {
      
      read_fds=master;
      if(select(fdmax+1, &read_fds, NULL, NULL, NULL)==-1) {
          perror("Serveur : problem select.");
          exit(4);
      }
     
     for(i=0; i<=fdmax; i++)
     {
         if(FD_ISSET(i, &read_fds)) {
             if(i==sock_fd)
             {
                 s_taille = sizeof(client_addr);
                 srvc_fd = accept(sock_fd, (struct sockaddr *) &client_addr, &s_taille);
                 
                 if (srvc_fd == -1) {
                     perror("accept");
                     continue;
                }
                
                FD_SET(srvc_fd, &master);
                if(fdmax<srvc_fd)
                {
                    fdmax=srvc_fd;
                }
                
                printf("Serveur: connexion d'un nouveau client\n");

             }
             else
             {
                 // reception msg OK du client
                 recv(i, head, 2, 0);
                 
                 num_cli=num_cli+1;
                                  
                 snprintf(msg, 50, "Bienvenue client :,%u,", htons((uint16_t) num_cli));
               
                 taille_msg=htons((uint16_t) strlen(msg));
                 memcpy(head, &taille_msg, 2);
                
                 send(i, head, 2, 0);
                 
                 if((send(i, msg, strlen(msg), 0)) == -1) {
                     perror("send");
                }
                
                printf("MSG envoyé : %s\n", msg);
                
                FD_CLR(i, &master);
                close(i);
             }
         }
     }
    
  }

  close(sock_fd);
  
  exit(0);
}

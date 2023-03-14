program generate_hofstadter_dispersion_matrix_for_w2dynamics

  implicit none

  integer, parameter :: q=3
  integer, parameter :: ksteps=100
  real(kind=8), parameter :: pi=3.141592653589793238440d0
  real(kind=8), parameter :: t=0.250d0
  real(kind=8), parameter :: B=1.0d0/3.0d0

  complex(kind=8), dimension(:,:), allocatable :: epsmat 

  character(len=1000) :: FormatString
  integer :: ikx,iky,l,lp
  real(kind=8) :: kx,ky

  !Allocate and initialize epsmat
  allocate(epsmat(1:q,1:q))
  do l=1,q
     do lp=1,q
        epsmat(l,lp)=dcmplx(0.0d0,0.0d0)
     enddo
  enddo
  write(FormatString,*)2*q
  FormatString='('//trim(adjustl(FormatString))//'f22.17)'

  open(10,file="Hk_Hofstadter.dat",form="formatted",status="replace")
  write(10,'(3I6)')4*ksteps*(ksteps/q),q,q

  do ikx=-ksteps+1,ksteps
     kx=Pi*dfloat(ikx)/dfloat(ksteps)
     do iky=-ksteps/q+1,ksteps/q
        ky=Pi*dfloat(iky)/dfloat(ksteps)
        !Construct dispersion matrix for given valuex of kx and ky
        if (q.gt.2) then
           epsmat(1,1)=dcmplx(-2.0d0*t*dcos(kx),0.0d0)
           epsmat(1,2)=dcmplx(-t,0.0d0)
           epsmat(1,q)=dcmplx(-t*dcos(dfloat(q)*ky),0.0d0)+ &
                dcmplx(0.0d0,-t*dsin(dfloat(q)*ky))
           epsmat(q,q)=dcmplx(-2.0d0*t* &
                dcos(kx+dfloat(q-1)*B*2.0d0*pi),0.0d0)
           epsmat(q,q-1)=dcmplx(-t,0.0d0)
           epsmat(q,1)=dcmplx(-t*dcos(dfloat(q)*ky),0.0d0)- &
                dcmplx(0.0d0,-t*dsin(dfloat(q)*ky))               
           do l=2,q-1
              epsmat(l,l)=dcmplx(-2.0d0*t* &
                   dcos(kx+dfloat(l-1)*B*2.0d0*Pi),0.0d0)
              epsmat(l,l-1)=dcmplx(-t,0.0d0)
              epsmat(l,l+1)=dcmplx(-t,0.0d0)
           enddo
        elseif (q.eq.2) then
           epsmat(1,1)=dcmplx(-2.0d0*t*dcos(kx),0.0d0)
           epsmat(1,2)=dcmplx(-t-t*dcos(dfloat(L)*ky),0.0d0)+ &
                dcmplx(0.0d0,-t*dsin(dfloat(L)*ky))
           epsmat(2,2)=dcmplx(-2.0d0*t*dcos(kx+B*2.0d0*Pi),0.0d0)
           epsmat(2,1)=dcmplx(-t-t*dcos(dfloat(2)*ky),0.0d0)- &
                dcmplx(0.0d0,-t*dsin(dfloat(2)*ky))
        else
           epsmat(1,1)=-2*t*(dcos(kx)+dcos(ky))
        endif
        write(10,'(3f17.10)')dfloat(ikx+ksteps-1)/dfloat(2*ksteps), &
             dfloat(iky+ksteps/q-1)/dfloat(2*(ksteps/q)),0.0d0
        do l=1,q
           write(10,FormatString)(dreal(epsmat(l,lp)),dimag(epsmat(l,lp)),lp=1,q)
        enddo
     enddo
  enddo

end program generate_hofstadter_dispersion_matrix_for_w2dynamics
